"""URL configuration for posts."""
from django.conf.urls import re_path
from posts.views import PostCreateView

urlpatterns = [
    re_path(r'^create/$', PostCreateView.as_view(), name='create'),
    re_path(r'^like/$', 'posts.views.like', name='like'),
]
