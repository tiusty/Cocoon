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
    set to hash them together, forming the url_slug
    """

    print("This stuff is all happening")

    if instance.url_slug is '':
        # concatenate multiple strings to guard against reversing
        hashable_string = "{0} {1} {2}".format(instance.id, instance.client.id, instance.tour_duration_seconds)

        # build the hash
        md5 = hashlib.md5()
        md5.update(hashable_string.encode('utf-8'))

        url_slug = slugify(md5.hexdigest())
        instance.url_slug = url_slug

