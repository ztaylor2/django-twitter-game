"""Database models."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from background_task import background


class UserProfile(models.Model):
    """The profile model."""

    ELIGIBILITY_CHOICES = (
        ('Yes', 'Y'),
        ('No', 'N'),
    )

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    karma = models.SmallIntegerField(default=100)
    eligibility = models.CharField(max_length=50,
                                   choices=ELIGIBILITY_CHOICES,
                                   default=ELIGIBILITY_CHOICES[0][0])
    time_ineligible = models.DateTimeField(null=True)
    correct_count = models.SmallIntegerField(default=0)


class Post(models.Model):
    """The model for a post."""

    VALIDITY_CHOICES = (
        ('NA', 'NA'),
        ('Yes', 'Y'),
        ('No', 'N'),
    )

    body = models.CharField(max_length=280)
    validated = models.CharField(max_length=50,
                                 choices=VALIDITY_CHOICES,
                                 default=VALIDITY_CHOICES[0][0])
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='photo')
    time_posted = models.DateTimeField(auto_now=False, auto_now_add=True)

    @property
    def total_likes(self):
        """Total likes for the post."""
        return self.like.count()

    @property
    def total_dislikes(self):
        """Total dislikes for the post."""
        return self.dislike.count()


class Like(models.Model):
    """The model for a like."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='like')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='like')


class Dislike(models.Model):
    """The model for a dislike."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='dislike')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='dislike')


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    """Create the profile when a user is created."""
    if kwargs['created']:
        profile = UserProfile(user=kwargs['instance'])
        profile.save()


@receiver(models.signals.post_save, sender=Post)
def new_post(sender, **kwargs):
    """Create the profile when a user is created."""
    post = kwargs['instance']
    determine_post_validity(post.id)


@background(schedule=3600)
def determine_post_validity(post_id):
    """Determine if the post is valid after an hour of voting."""
    post = Post.objects.get(id=post_id)
    determine_post_validation(post)
    assign_karma_points(post)


@background(schedule=86400)
def profile_eligibility_timer(profile_id):
    """After 24 hours make the profile eligible again."""
    user_profile = UserProfile.objects.get(id=profile_id)
    user_profile.karma = 20
    user_profile.eligibility = 'Yes'
    user_profile.save()


def determine_post_validation(post):
    """Determine if a post is validated."""
    if post.total_likes - post.total_dislikes > 0:
        post.validated = 'Yes'
    else:
        post.validated = 'No'
    post.save()


def incorrect_user(profile):
    """Handle when a user is incorrect."""
    profile.karma -= 10
    profile.correct_count = 0
    if profile.karma <= 0:
        profile.eligibility = 'No'
        profile.karma = 0
        profile_eligibility_timer(profile.id)
    profile.save()


def correct_user(profile):
    """Handle when a user is correct."""
    if profile.correct_count == 2:
        profile.karma += 20
    if profile.correct_count >= 3:
        profile.karma += 50
    profile.correct_count += 1
    profile.save()


def assign_karma_points(post):
    """Assign karma points after a post is validated."""
    if post.validated == 'No':
        for like in post.like.all():
            incorrect_user(like.user.profile)

        for dislike in post.dislike.all():
            correct_user(dislike.user.profile)

    if post.validated == 'Yes':
        for dislike in post.dislike.all():
            incorrect_user(dislike.user.profile)

        for like in post.like.all():
            correct_user(like.user.profile)
