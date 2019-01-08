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

    last_updated_feed = models.DateField(default=timezone.now)

    def __str__(self):
        return self.provider

    def save(self, *args, **kwargs):
        # Protect against multiple providers added via admin / command-line
        for provider in HomeProviderModel.objects.filter(provider=self.provider):
            if provider.pk is not self.pk:
                raise ValidationError("There should only be one {0} management object".format(self.provider))
        return super(HomeProviderModel, self).save(*args, **kwargs)

# This is used as a "hack" so that every abstract model class has a base class that contains
#   the update function. This way when the chain of super's is done being called, it will call
#   into this base class which will prevent the super function from breaking
class UpdateBase:
    def update(self, update_model):
        pass


class HouseLocationInformationModel(UpdateBase, models.Model):
    """
    Stores information regarding the location of the house
    """
    apartment_number = models.CharField(max_length=200, default="", blank=True)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    @property
    def full_address(self):
        return self.street_address + ", " + self.city + ", " \
               + self.state + " " + self.zip_code

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        :param update_model: (HouseLocationInformationModel) -> The model to use to update current model
        """
        super(HouseLocationInformationModel, self).update(update_model)
        self.apartment_number = update_model.apartment_number
        self.street_address = update_model.street_address
        self.city = update_model.city
        self.state = update_model.state
        self.zip_code = update_model.zip_code
        self.latitude = update_model.latitude
        self.longitude = update_model.longitude

    class Meta:
        abstract = True


class HouseInteriorAmenitiesModel(UpdateBase, models.Model):
    """
    Stores information about interior amenities
    """
    num_bathrooms = models.IntegerField(default=0)
    num_bedrooms = models.IntegerField(default=0)

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        :param update_model: (HouseInteriorAmenitiesModel) -> The model to use to update current model
        """
        super(HouseInteriorAmenitiesModel, self).update(update_model)
        self.num_bathrooms = update_model.num_bathrooms
        self.num_bedrooms = update_model.num_bedrooms

    class Meta:
        abstract = True


class HouseExteriorAmenitiesModel(UpdateBase, models.Model):
    """
    Contains all the information for homes about the Exterior Amenities
    """
    parking_spot = models.BooleanField(default=False)

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        :param update_model: (HouseExteriorAmenitiesModel) -> The model to use to update current model
        """
        super(HouseExteriorAmenitiesModel, self).update(update_model)
        self.parking_spot = update_model.parking_spot

    class Meta:
        abstract = True


class HouseManagementModel(UpdateBase, models.Model):
    """
    Contains all the data related to managing the house listing
    """
    remarks = models.TextField(default="", blank=True)
    listing_number = models.IntegerField(default=-1)  # The id of the home
    listing_provider = models.ForeignKey(HomeProviderModel)
    listing_agent = models.CharField(max_length=200, default="", blank=True)
    listing_office = models.CharField(max_length=200, default="", blank=True)  # The listing office, i.e William Raveis
    last_updated = models.DateField(default=timezone.now)

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        :param update_model: (HouseManagementModel) -> The model to use to update current model
        """
        super(HouseManagementModel, self).update(update_model)
        self.remarks = update_model.remarks
        self.listing_number = update_model.listing_number
        self.listing_provider = update_model.listing_provider
        self.listing_agent = update_model.listing_agent
        self.listing_office = update_model.listing_office
        self.last_updated = update_model.last_updated

    class Meta:
        abstract = True


class RentDatabaseModel(HouseManagementModel, HouseExteriorAmenitiesModel, HouseLocationInformationModel,
                        HouseInteriorAmenitiesModel):
    """
    This model stores all the information associated with a home
    """
    price = models.IntegerField(default=-1)
    home_type = models.ForeignKey('HomeTypeModel', on_delete=models.PROTECT)
    currently_available = models.BooleanField(default=False)

    def __str__(self):
        return self.full_address

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        Calls into all its inherited classes to update the corresponding fields
        :param update_model: (RentDatabaseModel) -> The model to use to update current model
        """
        super(RentDatabaseModel, self).update(update_model)
        self.price = update_model.price
        self.home_type = update_model.home_type
        self.currently_available = update_model.currently_available

    @property
    def price_string(self):
        return "$" + str(self.price)


def house_directory_path(instance, filename):
    return 'houseDatabase/{0}/{1}'.format(instance.house.id, filename)


class HousePhotos(models.Model):
    house = models.ForeignKey('RentDatabaseModel', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=house_directory_path)

    def __str__(self):
        return self.image.name

