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
    def update_posts(self):
        """Check if any posts are under consideration and update them if necessary."""
        posts_under_consideration = Post.objects.filter(validated='NA')
        if posts_under_consideration:
            for post in posts_under_consideration:
                minutes_since_creation = (datetime.now(timezone.utc) - post.time_posted).total_seconds() / 60
                if minutes_since_creation > 60:
                    self.determine_post_validation(post)
                    self.assign_karma_points(post)

    # def get_queryset(self):
    #     """Return the sitters ordered by sitter rank."""
    #     queryset = SitterProfile.objects.order_by('sitterrank__sitter_rank').reverse()
    #     if 'reviewfilter' in self.request.GET:
    #         queryset = queryset.filter(sitterrank__ratings_score__gte=self.request.GET['reviewfilter'])
    #     return queryset


from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse


# @login_required
# @require_POST
def like(request):
    """."""
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=user.id).exists():
            # user has already liked this post
            # remove like/user
            post.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a post
            post.likes.add(user)
            message = 'You liked this'

    ctx = {'likes_count': post.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
