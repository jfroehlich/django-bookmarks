# encoding: utf-8
from django import forms
from models import Bookmark

class BookmarkForm(forms.Form):
    address = forms.URLField()
    title = forms.CharField(widget=forms.TextInput(attrs={'size':'100'}))
    labels = forms.CharField(widget=forms.TextInput(attrs={'size':'100'}))
    notes = forms.CharField(required=False, widget=forms.Textarea)
    registration_required = forms.BooleanField(required=False)
    
    def clean_address(self):
        data = self.cleaned_data
        try:
            bookmark = Bookmark.objects.get(address=data['address'])
        except Bookmark.DoesNotExist:
            bookmark = None
        if bookmark and not data['obj_id'] == bookmark.id:
            raise forms.ValidationError("A bookmark with this address is already available.")
        return data['address']

