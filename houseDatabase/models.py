from django.db import models
import datetime
from django.utils import timezone


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
    _wash_dryer_in_home = models.BooleanField(default=False)
    _dish_washer = models.BooleanField(default=False)
    _bath = models.BooleanField(default=False)
    _num_bathrooms = models.IntegerField(default=0)
    _num_bedrooms = models.IntegerField(default=0)

    @property
    def air_conditioning(self):
        return self._air_conditioning

    @property
    def washer_dryer_in_home(self):
        return self._wash_dryer_in_home

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
        return self.address

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


class ZipCodeDictionary(models.Model):
    """
    The base Zip Code, aka 02476, for each base zip_code, there will be
    a bunch of associated zip codes via foreign key from ZipCodeDictionary model.
     The Base model should not have a commute_time or Commute_distance since it is in
     releation to nothing. Instead the child zip code identifies the relation
    """
    zip_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.get_zip_code()

    def get_zip_code(self):
        return self.zip_code

COMMUTE_TYPES = (
    ('driving', 'Driving'),
    ('transit', 'Transit'),
    ('walking', 'Walking'),
    ('biking', 'Biking'),
)

# This value determines how many days until the zip code value needs to be refreshed
zip_code_timedelta_value = 60


class ZipCodeDictionaryChild(models.Model):
    """
    This model class serves as an approximation for commute time/distance associated with
    zip_codes. This ZipCodeDictionary should be precomputed or should be populated periodically.
    """
    zip_code = models.CharField(max_length=20)
    base_zip_code = models.ForeignKey('ZipCodeDictionary', on_delete=models.CASCADE)
    commute_time = models.IntegerField(default=-1)
    commute_distance = models.IntegerField(default=-1)
    last_date_updated = models.DateField(default=timezone.now)
    commute_type = models.CharField(
        choices=COMMUTE_TYPES,
        max_length=15,
    )

    def __str__(self):
        return self.get_zip_code()

    def get_zip_code(self):
        return self.zip_code

    def get_base_zip_code(self):
        return self.base_zip_code

    # Commute time is stored in seconds so divide by 60 to get number of minutes
    def get_commute_time(self):
        return self.get_commute_time_seconds() / 60

    def get_commute_time_seconds(self):
        return self.commute_time

    # Commute distance is stored in meters so convert to miles
    def get_commute_distance(self):
        return self.get_commute_distance_meters() * 0.000621371

    def get_commute_distance_meters(self):
        return self.commute_distance

    def get_last_date_updated(self):
        return self.last_date_updated

    def test_recompute_date(self):
        """
        This function tests whether or not the zip code should be recalculated
        Currently, the zip_code should be recomputed if it is older than 2 months old
        :return:
        """
        if timezone.now().date() > self.get_last_date_updated() + timezone.timedelta(days=zip_code_timedelta_value):
            return True
        else:
            return False

    def get_commute_type(self):
        return self.commute_type
