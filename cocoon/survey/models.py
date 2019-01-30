# Import Django modules
from django.db import models
from django.utils.text import slugify

# Python Modules
import math

# Import cocoon models
from cocoon.userAuth.models import UserProfile
from cocoon.houseDatabase.models import HomeTypeModel, HomeProviderModel, RentDatabaseModel
from cocoon.commutes.models import CommuteType

# Import Global Variables
from config.settings.Global_Config import MAX_NUM_BATHROOMS, DEFAULT_RENT_SURVEY_NAME

# Import app constants
from .constants import MIN_PRICE_DELTA


class InitialSurveyModel(models.Model):
    """
    Stores the default information across all the surveys
    """
    name = models.CharField(max_length=200, default=DEFAULT_RENT_SURVEY_NAME)
    created = models.DateField(auto_now_add=True)
    user_profile = models.ForeignKey(UserProfile)
    number_of_tenants = models.IntegerField(default=1)
    favorites = models.ManyToManyField(RentDatabaseModel, related_name="favorite_list", blank=True)
    visit_list = models.ManyToManyField(RentDatabaseModel, related_name="visit_list", blank=True)
    url = models.SlugField(max_length=100)

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
        # Old url is saved to determine if the url for a survey changed
        old_url = self.url
        self.url = self.generate_slug()

        # If it is a new model or the url changed then delete any conflicting surveys
        if self.pk is None or old_url != self.url:
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
    num_bedrooms = models.IntegerField(default=0)
    max_bathrooms = models.IntegerField(default=MAX_NUM_BATHROOMS)
    min_bathrooms = models.IntegerField(default=0)
    home_type = models.ManyToManyField(HomeTypeModel)
    polygon_filter_type = models.IntegerField(default=0)
    is_move_asap = models.BooleanField(default=False)
    move_weight = models.IntegerField(default=0)

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
    max_price = models.IntegerField(default=0)
    desired_price = models.IntegerField(default=0)
    price_weight = models.IntegerField(default=0)

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


class HouseNearbyAmenitiesModel(models.Model):
    """
    Contains amenities that are near the house
    """
    wants_laundry_nearby = models.BooleanField(default=False)

    class Meta:
        abstract = True


class InteriorAmenitiesModel(models.Model):
    """
    Contains all the survey questions regarding the interior Amenities
    All Questions are hybrid weighted
    """
    wants_laundry_in_unit = models.BooleanField(default=False)
    wants_furnished = models.BooleanField(default=False)
    furnished_weight = models.IntegerField(default=0)
    wants_dogs = models.BooleanField(default=False)
    number_of_dogs = models.IntegerField(default=0)
    service_dogs = models.BooleanField(default=False)
    dog_size = models.CharField(max_length=200, blank=True, default="")
    breed_of_dogs = models.CharField(max_length=200, blank=True, default="")
    wants_cats = models.BooleanField(default=False)
    cat_weight = models.IntegerField(default=0)
    wants_hardwood_floors = models.BooleanField(default=False)
    hardwood_floors_weight = models.IntegerField(default=0)
    wants_AC = models.BooleanField(default=False)
    AC_weight = models.IntegerField(default=0)
    wants_dishwasher = models.BooleanField(default=False)
    dishwasher_weight = models.IntegerField(default=0)

    class Meta:
        abstract = True


class ExteriorAmenitiesModel(models.Model):
    """
    Contains all the survey questions regarding the exterior Amenities
    All Questions are hybrid weighted
    """
    wants_parking = models.BooleanField(default=False)
    number_of_cars = models.IntegerField(default=0)
    wants_laundry_in_building = models.BooleanField(default=False)
    wants_patio = models.BooleanField(default=False)
    patio_weight = models.IntegerField(default=0)
    wants_pool = models.BooleanField(default=False)
    pool_weight = models.IntegerField(default=0)
    wants_gym = models.BooleanField(default=False)
    gym_weight = models.IntegerField(default=0)
    wants_storage = models.BooleanField(default=False)
    storage_weight = models.IntegerField(default=0)

    class Meta:
        abstract = True


class RentingSurveyModel(InteriorAmenitiesModel, ExteriorAmenitiesModel, HouseNearbyAmenitiesModel,
                         PriceInformationModel, HomeInformationModel, InitialSurveyModel):
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


class TenantPersonalInformationModel(models.Model):
    first_name = models.CharField(max_length=200, blank=True, default="")
    last_name = models.CharField(max_length=200, blank=True, default="")
    occupation = models.CharField(max_length=200, blank=True, default="")
    other_occupation_reason = models.CharField(max_length=200, blank=True, default="")
    unemployed_follow_up = models.CharField(max_length=200, blank=True, default="")
    income = models.IntegerField(blank=True, null=True)
    credit_score = models.CharField(max_length=200, blank=True, default="")
    new_job = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        abstract = True


class DestinationsModel(models.Model):
    street_address = models.CharField(max_length=200, default="", blank=True)
    city = models.CharField(max_length=200, default="", blank=True)
    state = models.CharField(max_length=200, default="", blank=True)
    zip_code = models.CharField(max_length=200, default="", blank=True)

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
    max_commute = models.IntegerField(default=0)
    min_commute = models.IntegerField(default=0)
    commute_weight = models.IntegerField(default=0)
    commute_type = models.ForeignKey(CommuteType)
    traffic_option = models.BooleanField(default=False)

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


class TenantModel(DestinationsModel, CommuteInformationModel, TenantPersonalInformationModel):
    survey = models.ForeignKey(RentingSurveyModel, related_name="tenants")


class PolygonModel(models.Model):
    survey = models.ForeignKey(RentingSurveyModel, related_name='polygons', blank=True)


class VertexModel(models.Model):
    polygon = models.ForeignKey(PolygonModel, related_name='vertices', blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
