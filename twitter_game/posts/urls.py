"""URL configuration for posts."""
from django.conf.urls import re_path
from posts.views import PostCreateView
from . import views
from django.urls import path


urlpatterns = [
    re_path(r'^create/$', PostCreateView.as_view(), name='create'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
]


# from django.urls import path

# from . import views

# urlpatterns = [
#     path('', views.like, name='like'),
# ]