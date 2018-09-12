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

    @property
    def home_type(self):
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
    street_address_home = models.CharField(max_length=200)
    city_home = models.CharField(max_length=200)
    state_home = models.CharField(max_length=200)
    zip_code_home = models.CharField(max_length=200)
    price_home = models.IntegerField(default=-1)
    latitude_home = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude_home = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    @property
    def full_address(self):
        return self.street_address + ", " + self.city + ", " \
               + self.state + " " + self.zip_code

    @property
    def street_address(self):
        return self.street_address_home

    @street_address.setter
    def street_address(self, new_street_address):
        self.street_address_home = new_street_address

    @property
    def city(self):
        return self.city_home

    @city.setter
    def city(self, new_city):
        self.city_home = new_city

    @property
    def state(self):
        return self.state_home

    @state.setter
    def state(self, new_state):
        self.state_home = new_state

    @property
    def zip_code(self):
        if len(self.zip_code_home) > 5:
            return self.zip_code_home[:5]
        return self.zip_code_home

    @zip_code.setter
    def zip_code(self, new_zip_code):
        self.zip_code_home = new_zip_code

    @property
    def price(self):
        return self.price_home

    @price.setter
    def price(self, new_price):
        self.price_home = new_price

    @property
    def price_string(self):
        return "$" + str(self.price)

    @property
    def latitude(self):
        return self.latitude_home

    @latitude.setter
    def latitude(self, new_latitude):
        self.latitude_home = new_latitude

    @property
    def longitude(self):
        return self.longitude_home

    @longitude.setter
    def longitude(self, new_longitude):
        self.longitude_home = new_longitude

    class Meta:
        abstract = True


class InteriorAmenitiesModel(models.Model):
    """
    Contains all the information for homes about the Interior Amenities
    """
    air_conditioning_home = models.BooleanField(default=False)
    interior_washer_dryer_home = models.BooleanField(default=False)
    dish_washer_home = models.BooleanField(default=False)
    bath_home = models.BooleanField(default=False)
    num_bathrooms_home = models.IntegerField(default=0)
    num_bedrooms_home = models.IntegerField(default=0)

    @property
    def air_conditioning(self):
        return self.air_conditioning_home

    @property
    def interior_washer_dryer(self):
        return self.interior_washer_dryer_home

    @property
    def dish_washer(self):
        return self.dish_washer_home

    @property
    def bath(self):
        return self.bath_home

    @bath.setter
    def bath(self, new_bath):
        self.bath_home = new_bath

    @property
    def num_bathrooms(self):
        return self.num_bathrooms_home

    @num_bathrooms.setter
    def num_bathrooms(self, new_num_bathrooms):
        self.num_bathrooms_home = new_num_bathrooms

    @property
    def num_bedrooms(self):
        return self.num_bedrooms_home

    @num_bedrooms.setter
    def num_bedrooms(self, new_num_bedrooms):
        self.num_bedrooms_home = new_num_bedrooms

    class Meta:
        abstract = True


class BuildingExteriorAmenitiesModel(models.Model):
    """
    Contains all the information for homes about the Exterior Amenities
    """
    parking_spot_home = models.BooleanField(default=False)
    building_washer_dryer_home = models.BooleanField(default=False)
    elevator_home = models.BooleanField(default=False)
    handicap_access_home = models.BooleanField(default=False)
    pool_hot_tub_home = models.BooleanField(default=False)
    fitness_center_home = models.BooleanField(default=False)
    storage_unit_home = models.BooleanField(default=False)

    @property
    def parking_spot(self):
        return self.parking_spot_home

    @parking_spot.setter
    def parking_spot(self, has_parking_spot):
        self.parking_spot_home = has_parking_spot

    @property
    def building_washer_dryer(self):
        return self.building_washer_dryer_home

    @property
    def elevator(self):
        return self.elevator_home

    @property
    def handicap_access(self):
        return self.handicap_access_home

    @property
    def pool_hot_tub(self):
        return self.pool_hot_tub_home

    @property
    def fitness_center(self):
        return self.fitness_center_home

    @property
    def storage_unit(self):
        return self.storage_unit_home

    class Meta:
        abstract = True


class HomeManagementModel(models.Model):
    """
    Contains all the data related to managing the house listing
    """
    remarks_home = models.TextField(default="")
    listing_number_home = models.IntegerField(default=-1)  # The id of the home
    listing_provider_home = models.ForeignKey(HomeProviderModel)
    listing_agent_home = models.CharField(max_length=200, default="", blank=True)
    listing_office_home = models.CharField(max_length=200, default="", blank=True)  # The listing office, i.e William Raveis
    last_updated_home = models.DateField(default=timezone.now)

    @property
    def remarks(self):
        return self.remarks_home

    @remarks.setter
    def remarks(self, new_remarks):
        self.remarks_home = new_remarks

    @property
    def listing_number(self):
        return self.listing_number_home

    @listing_number.setter
    def listing_number(self, new_listing_number):
        self.listing_number_home = new_listing_number

    @property
    def listing_provider(self):
        return self.listing_provider_home

    @listing_provider.setter
    def listing_provider(self, new_listing_provider):
        self.listing_provider_home = new_listing_provider

    @property
    def listing_agent(self):
        return self.listing_agent_home

    @listing_agent.setter
    def listing_agent(self, new_listing_agent):
        self.listing_agent_home = new_listing_agent

    @property
    def listing_office(self):
        return self.listing_office_home

    @listing_office.setter
    def listing_office(self, new_listing_office):
        self.listing_office_home = new_listing_office

    @property
    def last_updated(self):
        return self.last_updated_home

    @last_updated.setter
    def last_updated(self, new_last_updated):
        self.last_updated_home = new_last_updated

    class Meta:
        abstract = True


class RentDatabaseModel(HomeManagementModel, BuildingExteriorAmenitiesModel, InteriorAmenitiesModel, HomeBaseModel):
    """
    This model stores all the information associated with a home
    """
    apartment_number_home = models.CharField(max_length=200, blank=True)
    home_type_home = models.ForeignKey('HomeTypeModel', on_delete=models.PROTECT)
    currently_available_home = models.BooleanField(default=False)

    def __str__(self):
        return self.full_address

    @property
    def home_type(self):
        return self.home_type_home

    @home_type.setter
    def home_type(self, new_home_type):
        self.home_type_home = new_home_type

    @property
    def apartment_number(self):
        return self.apartment_number_home

    @apartment_number.setter
    def apartment_number(self, new_apartment_number):
        self.apartment_number_home = new_apartment_number


    @property
    def currently_available(self):
        return self.currently_available_home

    @currently_available.setter
    def currently_available(self, is_available):
        """
        Sets whehter or not the home is currently available
        :param is_available: (Boolean) True if the home is available, false otherwise
        """
        self.currently_available_home = is_available


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



