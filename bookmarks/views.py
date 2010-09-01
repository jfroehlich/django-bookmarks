# encoding: utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from models import Label, Bookmark
from forms import BookmarkForm

str_to_labels = lambda x: [Label.objects.get_or_create(name=label)[0] for label in x.split()]
labels_to_str = lambda x: u"".join([label.name + " " for label in x])

# -- labels --

@login_required
def delete_label(request, label_name):
    label = get_object_or_404(Label, name=label_name)
    if request.method == 'POST':
        label.delete()
        return HttpResponseRedirect(reverse("bookmarks.views.bookmark_list", args=[]))
    request = RequestContext(request)
    return render_to_response('bookmarks/delete_label.html', {'label': label}, 
        context_instance=RequestContext(request))

# -- bookmarks --

def bookmark_list(request, label_str=u""):
    bookmarks = Bookmark.objects.filter(
        registration_required__in=[False, request.user.is_authenticated()])
    labels = []
    if label_str:
        labels = Label.objects.filter(name__in=label_str.split('+'))
        for label in labels:
            bookmarks = bookmarks.filter(labels__name=label.name)
    return object_list(request, queryset=bookmarks, template_object_name="bookmark",
        template_name="bookmarks/bookmark_list.html", paginate_by=10,
        extra_context={'selected_labels': labels, 'labels': Label.objects.all()})

@login_required
def create_bookmark(request):
    form = BookmarkForm()
    if request.method == 'GET' and request.GET:
        form = BookmarkForm(initial=request.GET)
    elif request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            labels = str_to_labels(data.pop('labels'))
            bookmark = Bookmark(**data)
            bookmark.author = request.user
            bookmark.save()
            bookmark.labels = labels
            bookmark.save()
            return HttpResponseRedirect(reverse("bookmarks.views.bookmark_list", args=[]))
    return render_to_response('bookmarks/bookmark_form.html', {'form': form, 
        'labels': Label.objects.all()}, context_instance=RequestContext(request))

@login_required
def edit_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    form = BookmarkForm(initial={
        'address': bookmark.address,
        'title': bookmark.title,
        'labels': labels_to_str(bookmark.labels.all()),
        'notes': bookmark.notes,
    })
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bookmark.title = data['title']
            bookmark.address = data['address']
            bookmark.notes = data['notes']
            bookmark.labels = str_to_labels(data['labels'])
            bookmark.save()
            return HttpResponseRedirect(reverse("bookmarks.views.view_bookmarks", args=[]))
    return render_to_response('bookmarks/bookmark_form.html', 
        {'form': form, 'bookmark': bookmark}, context_instance=RequestContext(request))
    
@login_required
def delete_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    if request.method == 'POST':
        bookmark.delete()
        return HttpResponseRedirect(reverse("bookmarks.views.view_bookmarks", args=[]))
    return render_to_response('bookmarks/delete_bookmark.html', 
        {'bookmark': bookmark}, context_instance=RequestContext(request))
