"""App views."""
# from django.shortcuts import render
from django.views.generic.edit import CreateView
from posts.models import Post, Like, Dislike
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create view."""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'posts/create.html'
    model = Post
    fields = ['body']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Assign the user to the foreign key in the model."""
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
@require_http_methods(["POST"])
def like(request):
    """Handle a user like."""
    user = request.user
    post_id = request.POST.get('post_id', None)
    post = get_object_or_404(Post, id=post_id)

    the_like, created = Like.objects.get_or_create(
        user=user,
        post=post)

    if created:
        message = 'You liked this'
        # if the user has already disliked the post remove the dislike
        if post.dislike.filter(user=user).exists():
            post.dislike.filter(user=user).delete()
    else:
        the_like.delete()
        message = 'You unliked this'

    likes_count = post.total_dislikes

    ctx = {'likes_count': likes_count, 'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


@login_required
@require_http_methods(["POST"])
def dislike(request):
    """Handle a user dislike."""
    user = request.user
    post_id = request.POST.get('post_id', None)
    post = get_object_or_404(Post, id=post_id)

    the_dislike, created = Dislike.objects.get_or_create(
        user=user,
        post=post)

    if created:
        message = 'You disliked this'
        # if the user has already liked the post remove the like
        if post.like.filter(user=user).exists():
            post.like.filter(user=user).delete()
    else:
        the_dislike.delete()
        message = 'You undisliked this'

    dislikes_count = post.total_dislikes

    ctx = {'dislikes_count': dislikes_count, 'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
