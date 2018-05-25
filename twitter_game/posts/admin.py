"""Admin."""
from django.contrib import admin
from posts.models import UserProfile, Post, Like, Dislike

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)
