# encoding: utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('bookmarks.views',
    (r'^$', 'latest_bookmarks', {}),
    (r'^create/$', 'create_bookmark', {}),
    (r'^(\d*)/$', 'view_bookmark', {}),
    (r'^(\d*)/edit/$', 'edit_bookmark', {}),
    (r'^(\d*)/delete/$', 'delete_bookmark', {}),
    
    (r'^labels/([\w\+]*)/$', 'view_label', {}),
    (r'^labels/(\d*)/delete/$', 'delete_label', {}),
)