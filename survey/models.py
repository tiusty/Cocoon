# Import django python modules
from django.db import models
from django.utils import timezone

# Import python modules
from enum import Enum
import math

# Import Global Variables
from Unicorn.settings.Global_Config import MAX_NUM_BATHROOMS, DEFAULT_RENT_SURVEY_NAME

# Import other models
from userAuth.models import UserProfile


class CommutePrecision(Enum):
    exact = 1
    approx = 2


HYBRID_WEIGHT_CHOICES = (
    (3, "Must have"),
    (2, "Really want"),
    (1, "Prefer to have"),
    (0, "I don't care"),
    (-1, "Prefer not to have"),
    (-2, "Really don't want"),
    (-3, "Don't want"),
)


class HomeType(models.Model):
    """
    Class stores all the different homes types
    This generates the multiple select field in the survey
    If another home gets added it needs to be added here in the HOME_TYPE
    tuples but also allowed past the query in the survey result view.
    """
    HOME_TYPE = (
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Condo', 'Condo'),
        ('Town House', 'Town House'),
    )
    homeType = models.CharField(
        choices=HOME_TYPE,
        max_length=200,
    )

    def __str__(self):
        return self.homeType


class InitialSurveyModel(models.Model):
    """
    Stores the default information across all the surveys
    """
    _name = models.CharField(max_length=200, default=DEFAULT_RENT_SURVEY_NAME)
    _survey_type = models.IntegerField(default=-1)
    _created = models.DateField(auto_now_add=True)
    _user_profile = models.ForeignKey(UserProfile)

    @property
    def name(self):
        return self._name

    @property
    def survey_type(self):
        return self._survey_type

    @property
    def created(self):
        return self._created

    @property
    def user_profile(self):
        return self._user_profile

    class Meta:
        abstract = True


class HomeInformationModel(models.Model):
    """
    Contains basic information about a home
    """
    _move_in_date_start = models.DateField(default=timezone.now)
    _move_in_date_end = models.DateField(default=timezone.now)
    _num_bedrooms = models.IntegerField(default=0)
    _max_bathrooms = models.IntegerField(default=MAX_NUM_BATHROOMS)
    _min_bathrooms = models.IntegerField(default=0)
    _home_type = models.ManyToManyField(HomeType)

    @property
    def move_in_date_start(self):
        return self._move_in_date_start

    @property
    def move_in_date_end(self):
        return self._move_in_date_end

    @property
    def num_bedrooms(self):
        return self._num_bedrooms

    @property
    def max_bathrooms(self):
        return self._max_bathrooms

    @property
    def min_bathrooms(self):
        return self._min_bathrooms

    @property
    def home_type(self):
        return self._home_type

    @property
    def home_types(self):
        home_type_set = self.home_type.all()
        if home_type_set.count() == 0:
            return "Not set"
        else:
            type_output = ""
            counter = 0
            for homeType in home_type_set:
                if counter == 0:
                    type_output = str(homeType)
                    counter += 1
                else:
                    type_output = str(homeType) + ", " + type_output

        return type_output

    class Meta:
        abstract = True


COMMUTE_TYPES = (
    ('driving', 'Driving'),
    ('transit', 'Transit'),
    ('bicycling', 'Biking'),
    ('walking', 'Walking')
)


class CommuteInformationModel(models.Model):
    """
    Contains all the commute information for a given home
    """
    _max_commute = models.IntegerField(default=0)
    _min_commute = models.IntegerField(default=0)
    _commute_weight = models.IntegerField(default=0)
    _commute_type = models.CharField(max_length=20, choices=COMMUTE_TYPES, default="driving")

    @property
    def max_commute(self):
        return self._max_commute

    @property
    def min_commute(self):
        return self._min_commute

    @property
    def commute_weight(self):
        return self._commute_weight

    @property
    def commute_type(self):
        return self._commute_type

    @property
    def commute_range(self):
        """
        Return the commute range as a string
        :return: String -> Commute range
        """
        if self.max_commute > 60:
            max_output = str(math.floor(self.max_commute / 60)) + " hours " + str(self.max_commute % 60) \
                         + " Minutes"
        else:
            max_output = str(self.max_commute) + " Minutes"
        if self.min_commute > 60:
            min_output = str(math.floor(self.min_commute / 60)) + " hours " + str(self.min_commute % 60) \
                         + " Minutes"
        else:
            min_output = str(self.min_commute) + " Minutes"

        return min_output + " - " + max_output

    class Meta:
        abstract = True


class PriceInformationModel(models.Model):
    """
    Contains all the price information for a given home
    """
    _max_price = models.IntegerField(default=0)
    _min_price = models.IntegerField(default=0)
    _price_weight = models.IntegerField(default=0)

    @property
    def max_price(self):
        return self._max_price

    @property
    def min_price(self):
        return self._min_price

    @property
    def price_weight(self):
        return self._price_weight

    @property
    def price_range(self):
        """
        Returns the price range
        :return: String -> Price range
        """
        return "${0} - ${1} ".format(self.min_price, self.max_price)

    class Meta:
        abstract = True


class InteriorAmenitiesModel(models.Model):
    """
    Contains all the survey questions regarding the interior amenities
    """
    _air_conditioning = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    _washer_dryer_in_home = models.IntegerField(default=0)
    _dish_washer = models.IntegerField(default=0)
    _bath = models.IntegerField(default=0)

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

    class Meta:
        abstract = True


class ExteriorAmenitiesModel(models.Model):
    """
    Contains all the survey questions regarding the building/Exterior Amenities
    All Questions are hybrid weighted
    """
    _parking_spot = models.IntegerField(default=0)
    _washer_dryer_in_building = models.IntegerField(default=0)
    _elevator = models.IntegerField(default=0)
    _handicap_access = models.IntegerField(default=0)
    _pool_hot_tub = models.IntegerField(default=0)
    _fitness_center = models.IntegerField(default=0)
    _storage_unit = models.IntegerField(default=0)

    @property
    def parking_spot(self):
        return self.parking_spot

    @property
    def washer_dryer_in_buiding(self):
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


class RentingSurveyModel(ExteriorAmenitiesModel, InteriorAmenitiesModel, PriceInformationModel, CommuteInformationModel,
                         HomeInformationModel, InitialSurveyModel):
    """
    Renting Survey Model is the model for storing data from the renting survey model.
    The user may take multiple surveys and it is linked to their User Profile

    Default name is stored unless the User changes it. Every time a survey is created the past
    default name is deleted to allow for the new one. Therefore, there is always a history
    of one survey
    """

    def __str__(self):
        user_short_name = self.user_profile.user.get_short_name()
        survey_name = self.name
        return "{0}: {1}".format(user_short_name, survey_name)


class Destinations(models.Model):
    _street_address = models.CharField(max_length=200)
    _city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    _zip_code = models.CharField(max_length=200)

    @property
    def street_address(self):
        return self._street_address

    @property
    def city(self):
        return self._city

    @property
    def zip_code(self):
        return self._zip_code[:5]

    @property
    def short_address(self):
        return "{0}, {1}".format(self.street_address, self.city)

    class Meta:
        abstract = True


# Used for the renting survey
class RentingDestinations(Destinations):
    survey = models.ForeignKey(RentingSurveyModel)

    def __str__(self):
        return self._street_address

