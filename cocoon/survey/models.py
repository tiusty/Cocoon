# Import Django modules
from django.db import models
from django.utils.text import slugify

# Python Modules
from enum import Enum
import math

# Import cocoon models
from cocoon.userAuth.models import UserProfile
from cocoon.houseDatabase.models import HomeTypeModel, HomeProviderModel
from cocoon.commutes.models import CommuteType

# Import Global Variables
from config.settings.Global_Config import MAX_NUM_BATHROOMS, DEFAULT_RENT_SURVEY_NAME, \
    HYBRID_WEIGHT_CHOICES

# Import app constants
from .constants import MIN_PRICE_DELTA


# TODO: Deprecate with new algorithm
class CommutePrecision(Enum):
    exact = 1
    approx = 2


class InitialSurveyModel(models.Model):
    """
    Stores the default information across all the surveys
    """
    name = models.CharField(max_length=200, default=DEFAULT_RENT_SURVEY_NAME)
    created_survey = models.DateField(auto_now_add=True)
    user_profile = models.ForeignKey(UserProfile)
    url = models.SlugField(max_length=100)
    provider = models.ManyToManyField(HomeProviderModel)

    @property
    def created(self):
        return self.created_survey

    @property
    def providers(self):
        provider_set = self.provider.all()
        if provider_set.count() == 0:
            return "Not set"
        else:
            type_output = ""
            counter = 0
            for provider in provider_set:
                if counter == 0:
                    type_output = str(provider)
                    counter += 1
                else:
                    type_output = str(provider) + ", " + type_output

        return type_output

    def generate_slug(self):
        """
        The slug should just be the name without spaces and with dashes instead.
        This is because spaces look weird in urls and should be dashes instead
        :return: (string) -> The generated slug
        """
        return slugify(self.name)

    # Adds functionality to the save method. This checks to see if a survey with the same slug
    #   for that user already exists. If it does then delete that survey and save the new one instead
    def save(self, *args, **kwargs):
        self.url = self.generate_slug()

        # Makes sure that the same slug doesn't exist for that user. If it does, then delete that survey
        if RentingSurveyModel.objects.filter(user_profile=self.user_profile)\
                .filter(url=self.url).exists():
            RentingSurveyModel.objects.filter(user_profile=self.user_profile)\
                .filter(url=self.url).delete()

        # When the model is being saved, make sure to generate the slug associated with the survey.
        # Since surveys with duplicate names are deleted, then it should guarantee uniqueness
        super().save(*args, **kwargs)  # Call the "real" save() method.

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

    @home_type.setter
    def home_type(self, new_home_type):
        self.home_type_survey = new_home_type

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
    desired_price_survey = models.IntegerField(default=0)
    price_weight_survey = models.IntegerField(default=0)

    @property
    def max_price(self):
        return self.max_price_survey

    @property
    def desired_price(self):
        return self.desired_price_survey

    @property
    def price_weight(self):
        return self.price_weight_survey

    @property
    def price_range(self):
        """
        Returns the price range
        :return: String -> Price range
        """
        return "${0} - ${1} ".format(self.desired_price, self.max_price)

    @property
    def min_price(self):
        return self.desired_price - MIN_PRICE_DELTA

    class Meta:
        abstract = True


class ExteriorAmenitiesModel(models.Model):
    """
    Contains all the survey questions regarding the building/Exterior Amenities
    All Questions are hybrid weighted
    """
    parking_spot_survey = models.IntegerField(choices=HYBRID_WEIGHT_CHOICES, default=0)

    @property
    def parking_spot(self):
        return self.parking_spot_survey

    class Meta:
        abstract = True


class RentingSurveyModel(ExteriorAmenitiesModel, PriceInformationModel,
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
