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
    APARTMENT = "ap"
    SINGLE_FAMILY = "sf"
    CONDO = "cn"
    OTHER = "ot"
    HOME_TYPE = (
        (APARTMENT, 'Apartment'),
        (SINGLE_FAMILY, 'Single Family'),
        (CONDO, 'Condo'),
        (OTHER, 'Other'),
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
    MLSPIN = "MLSPIN"
    YGL = "YGL"
    PROVIDER_TYPES = (
        (MLSPIN, 'MLSPIN'),
        (YGL, 'YGL'),
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
    furnished = models.BooleanField(default=False)
    hardwood_floors = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    dogs_allowed = models.BooleanField(default=False)
    cats_allowed = models.BooleanField(default=False)
    laundry_in_unit = models.BooleanField(default=False)
    dishwasher = models.BooleanField(default=False)

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        :param update_model: (HouseInteriorAmenitiesModel) -> The model to use to update current model
        """
        super(HouseInteriorAmenitiesModel, self).update(update_model)
        self.num_bathrooms = update_model.num_bathrooms
        self.num_bedrooms = update_model.num_bedrooms
        self.furnished = update_model.furnished
        self.hardwood_floors = update_model.hardwood_floors
        self.air_conditioning = update_model.air_conditioning
        self.dogs_allowed = update_model.dogs_allowed
        self.cats_allowed = update_model.cats_allowed
        self.laundry_in_unit = update_model.laundry_in_unit
        self.dishwasher = update_model.dishwasher

    class Meta:
        abstract = True


class HouseExteriorAmenitiesModel(UpdateBase, models.Model):
    """
    Contains all the information for homes about the Exterior Amenities
    """
    parking_spot = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    patio_balcony = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    storage = models.BooleanField(default=False)
    laundry_in_building = models.BooleanField(default=False)

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        :param update_model: (HouseExteriorAmenitiesModel) -> The model to use to update current model
        """
        super(HouseExteriorAmenitiesModel, self).update(update_model)
        self.parking_spot = update_model.parking_spot
        self.pool = update_model.pool
        self.patio_balcony = update_model.patio_balcony
        self.gym = update_model.gym
        self.storage = update_model.storage
        self.laundry_in_building = update_model.laundry_in_building

    class Meta:
        abstract = True


class HouseNearbyAmenitiesModel(UpdateBase, models.Model):
    """
    Contains all the nearby amenities associated with the home
    """
    laundromat_nearby = models.BooleanField(default=False)

    def update(self, update_model):
        """
        Given another model, updates current model with fields from the new model
        :param update_model: (HouseNearbyAmenitiesModel) -> The model to use to update current model
        """
        super(HouseNearbyAmenitiesModel, self).update(update_model)
        self.laundromat_nearby = update_model.laundromat_nearby

    class Meta:
        abstract = True


class HouseManagementModel(UpdateBase, models.Model):
    """
    Contains all the data related to managing the house listing
    """
    remarks = models.TextField(default="", blank=True)
    listing_number = models.IntegerField(default=-1)  # The id of the home
    listing_provider = models.ForeignKey(HomeProviderModel)
    listing_office_id = models.CharField(max_length=200, default="", blank=True)
    listing_agent_id = models.CharField(max_length=200, default="", blank=True)
    listing_agent_name = models.CharField(max_length=200, default="", blank=True)
    listing_agent_phone_1 = models.CharField(max_length=200, default="", blank=True)
    listing_agent_phone_2 = models.CharField(max_length=200, default="", blank=True)
    listing_agent_email = models.CharField(max_length=200, default="", blank=True)
    broker_notes = models.CharField(max_length=200, default="", blank=True)
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
        self.listing_agent_id = update_model.listing_agent_id
        self.listing_office_id = update_model.listing_office_id
        self.listing_agent_name = update_model.listing_agent_name
        self.listing_agent_phone_1 = update_model.listing_agent_phone_1
        self.listing_agent_phone_2 = update_model.listing_agent_phone_2
        self.listing_agent_email = update_model.listing_agent_email
        self.broker_notes = update_model.broker_notes
        self.last_updated = update_model.last_updated

    class Meta:
        abstract = True


class RentDatabaseModel(HouseManagementModel, HouseExteriorAmenitiesModel, HouseLocationInformationModel,
                        HouseInteriorAmenitiesModel, HouseNearbyAmenitiesModel):
    """
    This model stores all the information associated with a home
    """
    price = models.IntegerField(default=-1)
    home_type = models.ForeignKey('HomeTypeModel', on_delete=models.PROTECT)
    currently_available = models.BooleanField(default=False)
    date_available = models.DateField(default=timezone.now)

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
        self.date_available = update_model.date_available

    @property
    def price_string(self):
        return "$" + str(self.price)

    @property
    def on_market(self):
        """
        Returns whether or not the home is on market
        :return: (boolean) -> True: The home is currently on the market
                              False: The home is not on the market
        """
        # As long as the date of when the feed was updated matches the data
        # that the home was last updated, then the home is on market
        if self.listing_provider.last_updated_feed != self.last_updated:
            return False
        else:
            return True

    @staticmethod
    def create_house_database(home_type=None, listing_provider=None, currently_available=False,
                              price=1500, num_bedrooms=2, street_address="12 test Rd", city='SomeCity',
                              zip_code='02222', state='MA'):
        if home_type is None:
            home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
        if listing_provider is None:
            listing_provider = HomeProviderModel.objects.get_or_create(provider=HomeProviderModel.MLSPIN)[0]
        return RentDatabaseModel.objects.create(
            home_type=home_type,
            listing_provider=listing_provider,
            currently_available=currently_available,
            price=price,
            num_bedrooms=num_bedrooms,
            street_address=street_address,
            city=city,
            zip_code=zip_code,
            state=state,
        )


def house_directory_path(instance, filename):
    return 'houseDatabase/{0}/{1}'.format(instance.house.id, filename)


class HousePhotos(models.Model):
    house = models.ForeignKey('RentDatabaseModel', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=house_directory_path)

    def __str__(self):
        return self.image.name

