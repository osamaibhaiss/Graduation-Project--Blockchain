# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile if it does not exist
        Profile.objects.get_or_create(user=instance)
    else:
        # Update the profile if necessary
        instance.profile.save()
