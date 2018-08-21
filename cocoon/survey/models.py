# Import Django modules
from django.db import models

# Python Modules
from enum import Enum
import math

# Import cocoon models
from cocoon.userAuth.models import UserProfile
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType

# Import Global Variables
from config.settings.Global_Config import MAX_NUM_BATHROOMS, DEFAULT_RENT_SURVEY_NAME, \
    HYBRID_WEIGHT_CHOICES


# TODO: Deprecate with new algorithm
class CommutePrecision(Enum):
    exact = 1
    approx = 2


class InitialSurveyModel(models.Model):
    """
    Stores the default information across all the surveys
    """
    name_survey = models.CharField(max_length=200, default=DEFAULT_RENT_SURVEY_NAME)
    survey_type_survey = models.IntegerField(default=-1)
    created_survey = models.DateField(auto_now_add=True)
    user_profile_survey = models.ForeignKey(UserProfile)

    @property
    def name(self):
        return self.name_survey

    @property
    def survey_type(self):
        return self.survey_type_survey

    @survey_type.setter
    def survey_type(self, new_survey_type):
        self.survey_type_survey = new_survey_type

    @property
    def created(self):
        return self.created_survey

    @property
    def user_profile(self):
        return self.user_profile_survey

    @user_profile.setter
    def user_profile(self, new_user_profile):
        self.user_profile_survey = new_user_profile

    class Meta:
        abstract = True


class HomeInformationModel(models.Model):
    """
    Contains basic information about a home
    """
    num_bedrooms_survey = models.IntegerField(default=0)
    max_bathrooms_survey = models.IntegerField(default=MAX_NUM_BATHROOMS)
    min_bathrooms_survey = models.IntegerField(default=0)
    home_type_survey = models.ManyToManyField(HomeTypeModel)

    @property
    def num_bedrooms(self):
        return self.num_bedrooms_survey

    @property
    def max_bathrooms(self):
        return self.max_bathrooms_survey

    @property
    def min_bathrooms(self):
        return self.min_bathrooms_survey

    @property
    def home_type(self):
        return self.home_type_survey

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


class PriceInformationModel(models.Model):
    """
    Contains all the price information for a given home
    """
    max_price_survey = models.IntegerField(default=0)
    min_price_survey = models.IntegerField(default=0)
    price_weight_survey = models.IntegerField(default=0)

    @property
    def max_price(self):
        return self.max_price_survey

    @property
    def min_price(self):
        return self.min_price_survey

    @property
    def price_weight(self):
        return self.price_weight_survey

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
    air_conditioning_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    interior_washer_dryer_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    dish_washer_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    bath_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)

    @property
    def air_conditioning(self):
        return self.air_conditioning_survey

    @property
    def interior_washer_dryer(self):
        return self.interior_washer_dryer_survey

    @property
    def dish_washer(self):
        return self.dish_washer_survey

    @property
    def bath(self):
        return self.bath_survey

    class Meta:
        abstract = True


class ExteriorAmenitiesModel(models.Model):
    """
    Contains all the survey questions regarding the building/Exterior Amenities
    All Questions are hybrid weighted
    """
    parking_spot_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    building_washer_dryer_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    elevator_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    handicap_access_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    pool_hot_tub_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    fitness_center_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)
    storage_unit_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)

    @property
    def parking_spot(self):
        return self.parking_spot_survey

    @property
    def washer_dryer_in_building(self):
        return self.building_washer_dryer_survey

    @property
    def elevator(self):
        return self.elevator_survey

    @property
    def handicap_access(self):
        return self.handicap_access_survey

    @property
    def pool_hot_tub(self):
        return self.pool_hot_tub_survey

    @property
    def fitness_center(self):
        return self.fitness_center_survey

    @property
    def storage_unit(self):
        return self.storage_unit_survey

    class Meta:
        abstract = True


class RentingSurveyModel(ExteriorAmenitiesModel, InteriorAmenitiesModel, PriceInformationModel,
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


class DestinationsModel(models.Model):
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)

    @property
    def full_address(self):
        return "{0}, {1}, {2}, {3}".format(self.street_address, self.city, self.state, self.zip_code)

    @property
    def short_address(self):
        return "{0}, {1}".format(self.street_address, self.city)

    class Meta:
        abstract = True


class CommuteInformationModel(models.Model):
    """
    Contains all the commute information for a given home
    """
    max_commute = models.IntegerField()
    min_commute = models.IntegerField()
    commute_weight = models.IntegerField()
    commute_type = models.ForeignKey(CommuteType)

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


class RentingDestinationsModel(DestinationsModel, CommuteInformationModel):
    survey = models.ForeignKey(RentingSurveyModel)

    def __str__(self):
        return self.street_address
