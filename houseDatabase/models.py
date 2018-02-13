# Import Django modules
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Import Config file information
from Cocoon.settings.Global_Config import ZIP_CODE_TIMEDELTA_VALUE


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
    home_type_survey = models.CharField(
        unique=True,
        choices=HOME_TYPE,
        max_length=200,
    )

    def __str__(self):
        return self.home_type

    @property
    def home_type(self):
        return self.home_type_survey


class CommuteTypeModel(models.Model):
    """
    Class stores all the different commute types
    This generates a choice field in the survey
    If another commute type gets added, it should get added to the COMMUTE_TYPES field
    """

    COMMUTE_TYPES = (
        ('Driving', 'Driving'),
        ('Transit', 'Transit'),
        ('Walking', 'Walking'),
        ('Biking', 'Biking'),
    )
    commute_type_field = models.CharField(
        unique=True,
        choices=COMMUTE_TYPES,
        max_length=200,
    )

    def __str__(self):
        return self.commute_type

    @property
    def commute_type(self):
        return self.commute_type_field


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


class MLSpinDataModel(models.Model):
    """
    Contains all the data related to the MLS pin
    """
    remarks_home = models.TextField(default="")
    listing_number_home = models.IntegerField(default=-1)
    listing_provider_home = models.CharField(max_length=200)
    listing_agent_home = models.CharField(max_length=200)
    listing_office_home = models.CharField(max_length=200)
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


class RentDatabaseModel(MLSpinDataModel, BuildingExteriorAmenitiesModel, InteriorAmenitiesModel, HomeBaseModel):
    """
    This model stores all the information associated with a home
    """
    apartment_number_home = models.CharField(max_length=200)
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
    return 'houseDatabase_{0}/{1}'.format(instance.house.id, filename)


class HousePhotosModel(models.Model):
    house_photo = models.ForeignKey('RentDatabaseModel', on_delete=models.CASCADE)
    image_path_photo = models.CharField(default='housePhotos/5/pic1.jpg', max_length=200)

    def __str__(self):
        return self.image_path

    @property
    def house(self):
        return self.house_photo

    @property
    def image_path(self):
        return self.image_path_photo


class MlsManagementModel(models.Model):
    """
    Model that stores general database-wide information
    """

    last_updated_mls = models.DateField()

    def save(self, *args, **kwargs):
        if MlsManagementModel.objects.exists() and not self.pk:
            raise ValidationError("There should only be one MlsManagementModel object")
        return super(MlsManagementModel, self).save(*args, **kwargs)


class ZipCodeDictionaryParentModel(models.Model):
    """
    The base Zip Code, aka 02476, for each base zip_code, there will be
    a bunch of associated zip codes via foreign key from ZipCodeDictionaryParentModel model.
     The Base model should not have a commute_time_minutes or Commute_distance since it is in
     relation to nothing. Instead the child zip code identifies the relation
    """
    zip_code_parent = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.zip_code

    @property
    def zip_code(self):
        return self.zip_code_parent


class ZipCodeDictionaryChildModel(models.Model):
    """
    This model class serves as an approximation for commute time/distance associated with
    zip_codes. This ZipCodeDictionaryParentModel should be precomputed or should be populated periodically.
    """
    zip_code_child = models.CharField(max_length=20)
    parent_zip_code_child = models.ForeignKey('ZipCodeDictionaryParentModel', on_delete=models.CASCADE)
    commute_time_seconds_child = models.IntegerField(default=-1)
    commute_distance_meters_child = models.IntegerField(default=-1)
    last_date_updated_child = models.DateField(default=timezone.now)
    commute_type_child = models.ForeignKey('CommuteTypeModel', on_delete=models.PROTECT)

    def __str__(self):
        return self.zip_code

    @property
    def zip_code(self):
        return self.zip_code_child

    @property
    def parent_zip_code(self):
        return self.parent_zip_code_child

    @property
    def zip_code_parent(self):
        return self.parent_zip_code_child

    @property
    def commute_time_minutes(self):
        return self.commute_time_seconds / 60

    @property
    def commute_time_seconds(self):
        return self.commute_time_seconds_child

    @property
    def commute_distance_miles(self):
        return self.commute_distance_meters * 0.000621371

    @property
    def commute_distance_meters(self):
        return self.commute_distance_meters_child

    @property
    def last_date_updated(self):
        return self.last_date_updated_child

    @last_date_updated.setter
    def last_date_updated(self, new_last_date_updated):
        self.last_date_updated_child = new_last_date_updated

    @property
    def commute_type(self):
        return self.commute_type_child

    def zip_code_cache_still_valid(self):
        """
        This function tests whether or not the zip code should be recalculated
        Currently, the zip_code should be recomputed if it is older than 2 months old
        :return: Boolean: True -> The cache is still valid, False -> The cache is no longer valid
        """
        if timezone.now().date() > self.last_date_updated + timezone.timedelta(days=ZIP_CODE_TIMEDELTA_VALUE):
            return False
        else:
            return True
