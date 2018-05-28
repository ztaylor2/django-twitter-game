"""Views for app."""
from django.views.generic import ListView
from posts.models import Post


class HomeView(ListView):
    """Displayes all of the posts."""

    template_name = 'twitter_game/home.html'
    model = Post
    context_object_name = 'post_list'

    def get_queryset(self):
        """Return the posts ordered by time posted."""
        queryset = Post.objects.order_by('time_posted').reverse()
        return queryset
