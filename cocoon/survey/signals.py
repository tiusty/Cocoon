# Django module imports
from django.db.models.signals import pre_save
from django.dispatch import receiver

# App Module Imports
from .models import TenantModel

# Cocoon Module Imports
import cocoon.houseDatabase.maps_requester as geolocator
from config.settings.Global_Config import gmaps_api_key


@receiver(pre_save, sender=TenantModel)
def tenant_model_save(instance, *args, **kwargs):
    """
    This function runs pre-save of the new model.

    Specifically it is used now to check if the address of the tenant destination has changed.
        If it has then geocode the new address and store it in the tenant model
    """
    try:
        obj = TenantModel.objects.get(pk=instance.pk)
    except TenantModel.DoesNotExist:
        # If it is a new home then get the lat and long of the home for that home
        latlng = geolocator.maps_requester(gmaps_api_key).get_lat_lon_from_address(instance.full_address)
        if not latlng == -1:
            lat = latlng[0]
            lng = latlng[1]
            instance.latitude = lat
            instance.longitude = lng
    else:
        # If the home already exists then compare the old address values
        #   with the new one to determine if the address changed for the tenant
        if not obj.street_address == instance.street_address \
                or not obj.city == instance.city \
                or not obj.zip_code == instance.zip_code:

            # If the address changed then geocode the new address
            latlng = geolocator.maps_requester(gmaps_api_key).get_lat_lon_from_address(instance.full_address)
            if not latlng == -1:
                lat = latlng[0]
                lng = latlng[1]
                instance.latitude = lat
                instance.longitude = lng


