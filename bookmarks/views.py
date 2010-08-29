# encoding: utf-8
from models import Bookmark, Label

def view_label(request, label_name):
    raise NotImplementedError
    
def delete_label(request, label_name):
    raise NotImplementedError

def latest_bookmarks(request):
    raise NotImplementedError

def view_bookmark(request, bookmark_id):
    raise NotImplementedError

def create_bookmark(request, bookmark_id):
    raise NotImplementedError

def edit_bookmark(request, bookmark_id):
    raise NotImplementedError

def delete_bookmark(request, bookmark_id):
    raise NotImplementedError