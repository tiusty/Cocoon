from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userProfile", on_delete=models.CASCADE, default='none')
    test = models.CharField(max_length=200)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
            UserProfile.objects.create(user=instance, test="Please enter something")


post_save.connect(create_user_profile, sender=User)