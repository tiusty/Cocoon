from django.db import models
import datetime
from django.utils import timezone


not_set_char = "Not set"


class InteriorAmenities(models.Model):
    """
    Contains all the information for homes about the Interior Amenities
    """
    air_conditioning = models.BooleanField(default=False)
    wash_dryer_in_home = models.BooleanField(default=False)
    dish_washer = models.BooleanField(default=False)
    bath = models.BooleanField(default=False)
    num_bathrooms = models.IntegerField(default=0)
    num_bedrooms = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BuildingExteriorAmenities(models.Model):
    """
    Contains all the information for homes about the Exterior Amenities
    """
    parking_spot = models.BooleanField(default=False)
    washer_dryer_in_building = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    handicap_access = models.BooleanField(default=False)
    pool_hot_tub = models.BooleanField(default=False)
    fitness_center = models.BooleanField(default=False)
    storage_unit = models.BooleanField(default=False)

    class Meta:
        abstract = True


class RentDatabase(BuildingExteriorAmenities, InteriorAmenities):
    """
    This model stores all the information associated with a home
    """
    address = models.CharField(max_length=200, default=not_set_char)
    city = models.CharField(max_length=200, default=not_set_char)
    state = models.CharField(max_length=200, default=not_set_char)
    zip_code = models.CharField(max_length=200, default=not_set_char)
    price = models.IntegerField(default=-1)
    home_type = models.CharField(max_length=200, default=not_set_char)
    move_in_day = models.DateField(default=datetime.date.today)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lon = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return self.address

    def get_address(self):
        return self.address

    def full_address(self):
        return self.get_address() + ", " + self.get_city() + ", " + self.get_state() + " " + self.get_zip_code()

    def short_address(self):
        return self.get_address() + ", " + self.get_city()

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_zip_code(self):
        if len(self.zip_code) > 5:
            return self.zip_code[:5]
        return self.zip_code

    def get_price(self):
        return self.price

    def get_price_str(self):
        return "$" + str(self.get_price())

    def get_move_in_day(self):
        return self.move_in_day

    def get_num_bedrooms(self):
        return self.num_bedrooms

    def get_num_bathrooms(self):
        return self.num_bathrooms

    def get_home_type(self):
        return self.home_type

    def get_air_conditioning(self):
        return self.air_conditioning

    def get_wash_dryer_in_home(self):
        return self.wash_dryer_in_home

    def get_dish_washer(self):
        return self.dish_washer

    def get_bath(self):
        return self.bath

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_parking_spot(self):
        return self.parking_spot

    def get_washer_dryer_in_building(self):
        return self.washer_dryer_in_building

    def get_elevator(self):
        return self.elevator

    def get_handicap_access(self):
        return self.handicap_access

    def get_pool_hot_tub(self):
        return self.pool_hot_tub

    def get_fitness_center(self):
        return self.fitness_center

    def get_storage_unit(self):
        return self.storage_unit


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
        return self.commute_time / 60

    # Commute distance is stored in meters so convert to miles
    def get_commute_distance(self):
        return self.commute_distance * 0.000621371

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
