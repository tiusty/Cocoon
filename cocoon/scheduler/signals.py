# Django module imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# App module imports
from .models import ItineraryModel

# Import 3rd party libraries
import hashlib


@receiver(post_save, sender=ItineraryModel)
def itinerary_model_save(instance, *args, **kwargs):
    """
    This function runs post-save of the new model.
    Specifically, it is used to wait until the models other fields have been
    set to hash them together, forming the url
    """

    if instance.url is '':
        instance.url = instance.generate_slug()
        instance.save()

