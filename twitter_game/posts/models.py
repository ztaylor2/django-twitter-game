"""Database models."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


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
