"""Views for app."""
from django.views.generic import ListView
from posts.models import Post
from datetime import datetime, timezone


class HomeView(ListView):
    """Displayes all of the posts."""

    template_name = 'twitter_game/home.html'
    model = Post
    context_object_name = 'post_list'

    def determine_post_validation(self, post):
        """Determine if a post is validated."""
        likes = post.like.count()
        dislikes = post.dislike.count()
        if likes - dislikes > 0:
            post.validated = 'Yes'
        else:
            post.validated = 'No'
        post.save()

    def assign_karma_points(self, post):
        """Assign karma points after a post is validated."""
        if post.validated == 'No':
            for like in post.like.all():
                profile = like.user.profile
                profile.karma -= 10
                profile.save()
        # NEED TO ACCOUNT FOR ADDING KARMA PTS need to account for adding karma points

    # query for all posts under consideration, if they should no longer be under consideration run a funciton
    posts_under_consideration = Post.objects.filter(validated='NA')
    if posts_under_consideration:
        for post in posts_under_consideration:
            minutes_since_creation = (datetime.now(timezone.utc) - post.time_posted).total_seconds() / 60
            if minutes_since_creation > 60:
                determine_post_validation(post)
                assign_karma_points(post)

    # def get_queryset(self):
    #     """Return the sitters ordered by sitter rank."""
    #     queryset = SitterProfile.objects.order_by('sitterrank__sitter_rank').reverse()
    #     if 'reviewfilter' in self.request.GET:
    #         queryset = queryset.filter(sitterrank__ratings_score__gte=self.request.GET['reviewfilter'])
    #     return queryset
