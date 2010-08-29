# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User

class Label(models.Model):
    name = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name
    
    @models.permalink
    def path(self):
        return ('bookmarks.views.view_label', [self.name])

    @models.permalink
    def delete_path(self):
        return ('bookmarks.views.delete_label', [self.name])

class Bookmark(models.Model):
    address = models.URLField()
    title = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, null=True, blank=True, related_name="bookmarks")
    registration_required = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='bookmarks')
    
    class Meta:
        ordering = ('-created', 'title')
        unique_together = (('address', 'author'),)
    
    def __unicode__(self):
        return self.url
    
    @models.permalink
    def path(self):
        return ('bookmarks.views.view_bookmark', [self.title])

    @models.permalink
    def edit_path(self):
        return ('bookmarks.views.edit_bookmark', [self.title])

    @models.permalink
    def delete_path(self):
        return ('bookmarks.views.delete_bookmark', [self.title])

