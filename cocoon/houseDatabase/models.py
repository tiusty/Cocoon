# Import Django modules
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class HomeTypeModel(models.Model):
    """
    Class stores all the different homes types
    This generates the multiple select field in the survey
    If another home gets added it needs to be added here in the HOME_TYPE
    """
    HOME_TYPE = (
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Condo', 'Condo'),
        ('Town House', 'Town House'),
    )
    home_type = models.CharField(
        unique=True,
        choices=HOME_TYPE,
        max_length=200,
    )

    def __str__(self):
        return self.home_type


class HomeProviderModel(models.Model):
    """
    Class stores all the different providers that are used
    """
    PROVIDER_TYPES = (
        ('MLSPIN', 'MLSPIN'),
        ('YGL', 'YGL'),
    )

    provider = models.CharField(
        unique=True,
        choices=PROVIDER_TYPES,
        max_length=200,
    )

    def __str__(self):
        return self.provider


class HomeBaseModel(models.Model):
    """
    Contains all the base information for a home
    """
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    price = models.IntegerField(default=-1)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    num_bathrooms = models.IntegerField(default=0)
    num_bedrooms = models.IntegerField(default=0)

    @property
    def full_address(self):
        return self.street_address + ", " + self.city + ", " \
               + self.state + " " + self.zip_code

    @property
    def price_string(self):
        return "$" + str(self.price)

    class Meta:
        abstract = True


class BuildingExteriorAmenitiesModel(models.Model):
    """
    Contains all the information for homes about the Exterior Amenities
    """
    parking_spot = models.BooleanField(default=False)

    class Meta:
        abstract = True


class HomeManagementModel(models.Model):
    """
    Contains all the data related to managing the house listing
    """
    remarks = models.TextField(default="", blank=True)
    listing_number = models.IntegerField(default=-1)  # The id of the home
    listing_provider = models.ForeignKey(HomeProviderModel)
    listing_agent = models.CharField(max_length=200, default="", blank=True)
    listing_office = models.CharField(max_length=200, default="", blank=True)  # The listing office, i.e William Raveis
    last_updated = models.DateField(default=timezone.now)

    class Meta:
        abstract = True


class RentDatabaseModel(HomeManagementModel, BuildingExteriorAmenitiesModel, HomeBaseModel):
    """
    This model stores all the information associated with a home
    """
    apartment_number = models.CharField(max_length=200, blank=True)
    home_type = models.ForeignKey('HomeTypeModel', on_delete=models.PROTECT)
    currently_available = models.BooleanField(default=False)

    def __str__(self):
        return self.full_address


def house_directory_path(instance, filename):
    return 'houseDatabase/{0}/{1}'.format(instance.house.id, filename)


class HousePhotos(models.Model):
    house = models.ForeignKey('RentDatabaseModel', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=house_directory_path)

    def __str__(self):
        return self.image.name


class MlsManagementModel(models.Model):
    """
    Model that stores general mls information information
    """

    last_updated_mls = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if MlsManagementModel.objects.exists() and not self.pk:
            raise ValidationError("There should only be one MlsManagementModel object")
        return super(MlsManagementModel, self).save(*args, **kwargs)


class YglManagementModel(models.Model):
    """
    Model that stores general ygl information information
    """

    last_updated_ygl = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if YglManagementModel.objects.exists() and not self.pk:
            raise ValidationError("There should only be one MlsManagementModel object")
        return super(YglManagementModel, self).save(*args, **kwargs)



