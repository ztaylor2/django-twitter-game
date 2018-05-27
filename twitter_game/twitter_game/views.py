"""Views for app."""
from django.views.generic import ListView
from posts.models import Post, UserProfile
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

    def incorrect_user(self, profile):
        """Handle when a user is incorrect."""
        profile.karma -= 10
        profile.correct_count = 0
        if profile.karma <= 0:
            profile.eligibility = 'No'
            profile.time_ineligible = datetime.now(timezone.utc)
            profile.karma = 0
        profile.save()

    def correct_user(self, profile):
        """Handle when a user is correct."""
        if profile.correct_count == 2:
            profile.karma += 20
        if profile.correct_count >= 3:
            profile.karma += 50
        profile.correct_count += 1
        profile.save()

    def assign_karma_points(self, post):
        """Assign karma points after a post is validated."""
        if post.validated == 'No':
            for like in post.like.all():
                self.incorrect_user(like.user.profile)

            for dislike in post.dislike.all():
                self.correct_user(dislike.user.profile)

        if post.validated == 'Yes':
            for dislike in post.dislike.all():
                self.incorrect_user(dislike.user.profile)

            for like in post.like.all():
                self.correct_user(like.user.profile)

    def update_posts(self):
        """Check if any posts are under consideration and update them if necessary."""
        posts_under_consideration = Post.objects.filter(validated='NA')
        if posts_under_consideration:
            for post in posts_under_consideration:
                minutes_since_creation = (datetime.now(timezone.utc) - post.time_posted).total_seconds() / 60
                if minutes_since_creation > 1:
                    self.determine_post_validation(post)
                    self.assign_karma_points(post)

    def update_users(self):
        """Update the eligibility of the users."""
        users_ineligible = UserProfile.objects.filter(eligibility='No')
        if users_ineligible:
            for user_profile in users_ineligible:
                minutes_since_ineligible = (datetime.now(timezone.utc) - user_profile.time_ineligible).total_seconds() / 60
                if minutes_since_ineligible > 60 * 24:
                    user_profile.karma = 20
                    user_profile.eligibility = 'Yes'
                    user_profile.save()

    def get_queryset(self):
        """Return the posts ordered by time posted."""
        self.update_users()
        self.update_posts()
        queryset = Post.objects.order_by('time_posted').reverse()
        return queryset
