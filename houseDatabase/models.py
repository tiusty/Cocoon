# Import Django modules
from django.db import models
from django.utils import timezone

# Import python modules
import datetime

# Import Config file information
from Unicorn.settings.Global_Config import COMMUTE_TYPES, ZIP_CODE_TIMEDELTA_VALUE


class HomeBase(models.Model):
    """
    Contains all the base information for a home
    """
    _street_address_home = models.CharField(max_length=200)
    _city_home = models.CharField(max_length=200)
    _state_home = models.CharField(max_length=200)
    _zip_code_home = models.CharField(max_length=200)
    _price_home = models.IntegerField(default=-1)
    _latitude_home = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    _longitude_home = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    @property
    def full_address(self):
        return self.street_address + ", " + self.city + ", " \
               + self.state + " " + self.zip_code

    @property
    def street_address(self):
        return self._street_address_home

    @property
    def city(self):
        return self._city_home

    @property
    def state(self):
        return self._state_home

    @property
    def zip_code(self):
        if len(self._zip_code_home) > 5:
            return self._zip_code_home[:5]
        return self._zip_code_home

    @property
    def price(self):
        return self._price_home

    @property
    def price_string(self):
        return "$" + str(self.price)

    @property
    def latitude(self):
        return self._latitude_home

    @property
    def longitude(self):
        return self._longitude_home

    class Meta:
        abstract = True


class InteriorAmenities(models.Model):
    """
    Contains all the information for homes about the Interior Amenities
    """
    _air_conditioning = models.BooleanField(default=False)
    _washer_dryer_in_home = models.BooleanField(default=False)
    _dish_washer = models.BooleanField(default=False)
    _bath = models.BooleanField(default=False)
    _num_bathrooms = models.IntegerField(default=0)
    _num_bedrooms = models.IntegerField(default=0)

    @property
    def air_conditioning(self):
        return self._air_conditioning

    @property
    def washer_dryer_in_home(self):
        return self._washer_dryer_in_home

    @property
    def dish_washer(self):
        return self._dish_washer

    @property
    def bath(self):
        return self._bath

    @property
    def num_bathrooms(self):
        return self._num_bathrooms

    @property
    def num_bedrooms(self):
        return self._num_bedrooms

    class Meta:
        abstract = True


class BuildingExteriorAmenities(models.Model):
    """
    Contains all the information for homes about the Exterior Amenities
    """
    _parking_spot = models.BooleanField(default=False)
    _washer_dryer_in_building = models.BooleanField(default=False)
    _elevator = models.BooleanField(default=False)
    _handicap_access = models.BooleanField(default=False)
    _pool_hot_tub = models.BooleanField(default=False)
    _fitness_center = models.BooleanField(default=False)
    _storage_unit = models.BooleanField(default=False)

    @property
    def parking_spot(self):
        return self._parking_spot

    @property
    def washer_dryer_in_building(self):
        return self._washer_dryer_in_building

    @property
    def elevator(self):
        return self._elevator

    @property
    def handicap_access(self):
        return self._handicap_access

    @property
    def pool_hot_tub(self):
        return self._pool_hot_tub

    @property
    def fitness_center(self):
        return self._fitness_center

    @property
    def storage_unit(self):
        return self._storage_unit

    class Meta:
        abstract = True


class MLSpinData(models.Model):
    """
    Contains all the data related to the MLS pin
    """
    _remarks = models.TextField(default="")
    _listing_number = models.IntegerField(default=-1)
    _listing_provider = models.CharField(max_length=200)
    _listing_agent = models.CharField(max_length=200)
    _listing_office = models.CharField(max_length=200)

    @property
    def remarks(self):
        return self._remarks

    @property
    def listing_number(self):
        return self._listing_number

    @property
    def listing_provider(self):
        return self._listing_provider

    @property
    def listing_agent(self):
        return self._listing_agent

    @property
    def listing_office(self):
        return self._listing_office

    class Meta:
        abstract = True


class RentDatabase(MLSpinData, BuildingExteriorAmenities, InteriorAmenities, HomeBase):
    """
    This model stores all the information associated with a home
    """
    _apartment_number = models.CharField(max_length=200)
    _home_type = models.CharField(max_length=200)
    _move_in_day = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.full_address

    @property
    def move_in_day(self):
        return self._move_in_day

    @property
    def home_type(self):
        return self._home_type

    @property
    def apartment_number(self):
        return self._apartment_number


def house_directory_path(instance, filename):
    return 'houseDatabase_{0}/{1}'.format(instance.house.id, filename)


class HousePhotos(models.Model):
    house = models.ForeignKey('RentDatabase', on_delete=models.CASCADE)
    image_path = models.CharField(default='housePhotos/5/pic1.jpg', max_length=200)

    def __str__(self):
        return self.get_image_path()

    def get_image_path(self):
        return self.image_path


class ZipCodeDictionaryParent(models.Model):
    """
    The base Zip Code, aka 02476, for each base zip_code, there will be
    a bunch of associated zip codes via foreign key from ZipCodeDictionaryParent model.
     The Base model should not have a commute_time_minutes or Commute_distance since it is in
     releation to nothing. Instead the child zip code identifies the relation
    """
    _zip_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.zip_code

    @property
    def zip_code(self):
        return self._zip_code


class ZipCodeDictionaryChild(models.Model):
    """
    This model class serves as an approximation for commute time/distance associated with
    zip_codes. This ZipCodeDictionaryParent should be precomputed or should be populated periodically.
    """
    _zip_code = models.CharField(max_length=20)
    _base_zip_code = models.ForeignKey('ZipCodeDictionaryParent', on_delete=models.CASCADE)
    _commute_time = models.IntegerField(default=-1)  # In seconds
    _commute_distance = models.IntegerField(default=-1)  # In Meters
    _last_date_updated = models.DateField(default=timezone.now)
    _commute_type = models.CharField(
        choices=COMMUTE_TYPES,
        max_length=15,
    )

    def __str__(self):
        return self.zip_code

    @property
    def zip_code(self):
        return self._zip_code

    @property
    def zip_code_parent(self):
        return self._base_zip_code

    @property
    def commute_time_minutes(self):
        return self.commute_time_seconds / 60

    @property
    def commute_time_seconds(self):
        return self._commute_time

    @property
    def commute_distance_miles(self):
        return self.commute_distance_meters * 0.000621371

    @property
    def commute_distance_meters(self):
        return self._commute_distance

    @property
    def last_date_updated(self):
        return self._last_date_updated

    @property
    def commute_type(self):
        return self._commute_type

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
