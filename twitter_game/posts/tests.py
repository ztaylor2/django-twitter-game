"""Test the posts app."""
from django.test import TestCase
from posts.models import UserProfile, Post, Like, Dislike
from django.contrib.auth.models import User


class PostTest(TestCase):
    """Test the post functionality."""

    def setUp(self):
        """Setup database with post with likes."""
        user = User(password='potatoes',
                    username='zach',
                    email='zach@example.com')
        user.save()

        post = Post(body='The body of a post.', user=user)
        post.save()

        like = Like(post=post,
                    user=user)
        like.save()

        dislike = Dislike(post=post,
                          user=user)
        dislike.save()

    def test_user_created_has_karma(self):
        """Test that a user is created and has 100 karma."""
        user = User.objects.get(username='zach')
        self.assertEqual(user.profile.karma, 100)
        self.assertEqual(user.profile.eligibility, 'Yes')

    def test_post_is_created_and_has_like_and_dislike(self):
        """Test that a post model instance is created by setup."""
        post = Post.objects.get(id=1)
        self.assertEqual(post.body, 'The body of a post.')
        self.assertEqual(post.like.count(), 1)
        self.assertEqual(post.dislike.count(), 1)
        self.assertEqual(post.validated, 'NA')
        self.assertEqual(post.like.all()[0].user.username, 'zach')
