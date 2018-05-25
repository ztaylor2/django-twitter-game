"""App views."""
from django.shortcuts import render
from django.views.generic.edit import CreateView
from posts.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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
