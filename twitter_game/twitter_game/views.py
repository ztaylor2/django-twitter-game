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
        if post.total_likes - post.total_dislikes > 0:
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
                profile.correct_count = 0
                profile.save()

            for dislike in post.dislike.all():
                profile = dislike.user.profile
                if profile.correct_count == 2:
                    profile.karma += 20
                if profile.correct_count >= 3:
                    profile.karma += 50
                profile.correct_count += 1
                profile.save()

        if post.validated == 'Yes':
            for dislike in post.dislike.all():
                profile = dislike.user.profile
                profile.karma -= 10
                profile.correct_count = 0
                profile.save()

            for like in post.like.all():
                profile = like.user.profile
                if profile.correct_count == 2:
                    profile.karma += 20
                if profile.correct_count >= 3:
                    profile.karma += 50
                profile.correct_count += 1
                profile.save()

    def update_posts(self):
        """Check if any posts are under consideration and update them if necessary."""
        posts_under_consideration = Post.objects.filter(validated='NA')
        if posts_under_consideration:
            for post in posts_under_consideration:
                minutes_since_creation = (datetime.now(timezone.utc) - post.time_posted).total_seconds() / 60
                if minutes_since_creation > 1:
                    self.determine_post_validation(post)
                    self.assign_karma_points(post)

    def get_queryset(self):
        """Return the sitters ordered by sitter rank."""
        self.update_posts()
        queryset = Post.objects.order_by('time_posted').reverse()
        return queryset
