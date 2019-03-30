# Import Django modules
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Import cocoon models
from cocoon.userAuth.models import UserProfile
from cocoon.houseDatabase.models import HomeTypeModel, HomeProviderModel, RentDatabaseModel
from cocoon.commutes.models import CommuteType

# Import Global Variables
from config.settings.Global_Config import MAX_NUM_BATHROOMS

# Import third party libraries
import hashlib
from datetime import timedelta

# Import app constants
from .constants import MIN_PRICE_DELTA

# Load the logger
import logging
logger = logging.getLogger(__name__)


class InitialSurveyModel(models.Model):
    """
    Stores the default information across all the surveys
    """
    created = models.DateField(auto_now_add=True)
    user_profile = models.ForeignKey(UserProfile)
    number_of_tenants = models.IntegerField(default=1)
    favorites = models.ManyToManyField(RentDatabaseModel, related_name="favorite_list", blank=True)
    visit_list = models.ManyToManyField(RentDatabaseModel, related_name="visit_list", blank=True)
    url = models.SlugField(max_length=100, default="not-set")

    def generate_slug(self):
        """
        Generates a unique slug for the survey
        :return: (string) -> The generated slug
        """

        # Create the unique string that will be hashed
        # Multiple things are added so people can't reverse hash the id
        hashable_string = "{0}{1}{2}{3}".format(self.user_profile.user.id, self.created, self.number_of_tenants, self.id)

        # Create the md5 object
        m = hashlib.md5()

        # Add the string to the hash function
        m.update(hashable_string.encode('utf-8'))

        # Now return the has has the url
        return slugify(m.hexdigest())

    class Meta:
        abstract = True


class SurveyUpdateInformation(models.Model):
    """
    Stores information about rerunning the survey and updating the user about changes
    """
    last_updated = models.DateField(default=timezone.now)
    update_frequency = models.IntegerField(default=2)
    wants_update = models.BooleanField(default=False)
    score_threshold = models.IntegerField(default=70)
    num_home_threshold = models.IntegerField(default=2)
    blacklisted_homes = models.ManyToManyField(RentDatabaseModel, related_name="blacklisted_homes", blank=True)

    def blacklist_home(self, home):
        """
        Adds a home to the blacklist field.

        That way that home won't trigger an email again.
        :param home: (RentDatabaseModel) -> The home that is being blacklisted
        """
        self.blacklisted_homes.add(home)

    def check_home_in_blacklist(self, home):
        """
        Checks to see if a home is in the blacklist
        :param home: (RentDataBaseModel) -> The home that is being checked
        :return: (Boolean) -> True: The home is in the blacklist
                              False: The home is not in the blacklist
        """
        return self.blacklisted_homes.filter(id=home.id).exists()

    def determine_threshold_trigger(self, home_scores):
        """
        Determines if the threshold trigger is reached and if so then it
            returns those homes
        :param home_scores: (list(HomeScore)) -> A list of the homes
        :return:
        """
        homes_over_threshold = []
        if len(home_scores) >= self.num_home_threshold:
            for home in home_scores:
                if not self.check_home_in_blacklist(home.home):
                    if home.percent_match >= self.score_threshold:
                        homes_over_threshold.append(home)

        if len(homes_over_threshold) >= self.num_home_threshold:
            return homes_over_threshold
        else:
            return []

    def ready_to_update_user(self):
        """
        Determines if the survey is ready to be updated based on the last time the user was
            updated and the frequency they put
        """
        if self.last_updated + timedelta(days=self.update_frequency) <= timezone.now().date():
            return True
        else:
            return False

    class Meta:
        abstract = True


class HomeInformationModel(models.Model):
    """
    Contains basic information about a home
    """
    num_bedrooms_bit_masked = models.IntegerField(default=0)
    max_bathrooms = models.IntegerField(default=MAX_NUM_BATHROOMS)
    min_bathrooms = models.IntegerField(default=0)
    home_type = models.ManyToManyField(HomeTypeModel)
    polygon_filter_type = models.IntegerField(default=0)
    move_weight = models.IntegerField(default=0)
    earliest_move_in = models.DateField(blank=True, null=True)
    latest_move_in = models.DateField(blank=True, null=True)

    @property
    def num_bedrooms(self):
        """
        The num_bedrooms_bit_masked variable sets the bit corresponding to the number of
            rooms needed. The num of rooms needed is the index of the number

            i.e if the user wants 1 and 3 rooms then the value would be 101 in decimal
                if the user wants 2 + 3 + 4 rooms then the value would be 11100 in decimal

            Therefore this function takes the bit mask of bedrooms and converts it into a python
                list of all the number of bedrooms desired
                i.e turns 11100 -> [2, 3, 4]
        :return: (list(ints)) -> The list of ints for the rooms numbers the user wants
        """
        still_converting = True
        bedroom_mask = self.num_bedrooms_bit_masked
        bits_set = []
        # Convert the decimal into binary as a list
        while still_converting:
            if bedroom_mask == 0 or bedroom_mask == 1:
                still_converting = False
            reminder = bedroom_mask % 2
            bedroom_mask = ((bedroom_mask - reminder)/2)
            bits_set.append(reminder)

        bedrooms_set = []
        counter = 0
        # See which bits were set. If it is a 1, then that number of bedrooms is desired
        for value in bits_set:
            if value == 1:
                bedrooms_set.append(counter)
            counter += 1

        return bedrooms_set

    @num_bedrooms.setter
    def num_bedrooms(self, num_bedrooms_list):
        """
        Since the num_bedrooms_bit_masked is stored as described above, this
            converts the list of bedrooms the user wants into the value that corresponds
            to the desired room numbers. Since the indicator of the room numbers is setting
            that bit to 1, the value is created by adding together the powers of two of
            the values of room number the user wants
        :param num_bedrooms_list: (list(ints)) -> The room numbers the user wants
        """
        binary_mask = 0
        # A set is used to make sure there isn't duplicates
        for num in set(num_bedrooms_list):
            binary_mask += 2 ** num
        self.num_bedrooms_bit_masked = binary_mask

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
    laundry_nearby_weight = models.IntegerField(default=0)

    class Meta:
        abstract = True


class InteriorAmenitiesModel(models.Model):
    """
    Contains all the survey questions regarding the interior Amenities
    All Questions are hybrid weighted
    """
    wants_laundry_in_unit = models.BooleanField(default=False)
    laundry_in_unit_weight = models.IntegerField(default=0)
    wants_furnished = models.BooleanField(default=False)
    furnished_weight = models.IntegerField(default=0)
    wants_dogs = models.BooleanField(default=False)
    dog_weight = models.IntegerField(default=0)
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
    laundry_in_building_weight = models.IntegerField(default=0)
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
                         PriceInformationModel, HomeInformationModel, SurveyUpdateInformation, InitialSurveyModel):
    """
    Renting Survey Model is the model for storing data from the renting survey model.
    The user may take multiple surveys and it is linked to their User Profile

    Default name is stored unless the User changes it. Every time a survey is created the past
    default name is deleted to allow for the new one. Therefore, there is always a history
    of one survey
    """

    @property
    def survey_name(self):
        """
        Generates the name for the survey based on the tenants
        """
        num_of_tenants = self.tenants.count()
        if num_of_tenants is 1:
            if self.user_profile.user.is_broker:
                return "{0} {1}".format(self.tenants.first().first_name, self.tenants.first().last_name[0])
            else:
                return "Just Me"
        else:
            counter = 1
            survey_name = ""
            # need to order the tenants, because the first tenant is the user of the account
            for tenant in self.tenants.order_by('id').reverse():
                if counter == num_of_tenants - 1:
                    survey_name = "{0}{1} {2} ".format(survey_name, tenant.first_name, tenant.last_name[0])
                elif counter == num_of_tenants:
                    if self.user_profile.user.is_broker:
                        survey_name = "{0}and {1} {2}".format(survey_name, tenant.first_name, tenant.last_name[0])
                    else:
                        survey_name = "{0}and I".format(survey_name)
                elif counter != num_of_tenants:
                    survey_name = "{0}{1} {2}, ".format(survey_name, tenant.first_name, tenant.last_name[0])
                counter += 1
            return survey_name

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=None, earliest_move_in=None, latest_move_in=None, move_weight=0,
                      wants_laundry_in_building=False, wants_laundry_in_unit=False, laundry_in_building_weight=0,
                      laundry_in_unit_weight=0, home_type=None, score_threshold=50, update_frequency=1,
                      wants_update=False, num_home_threshold=3, price_weight=0):
        if num_bedrooms is None:
            num_bedrooms = [2]
        if earliest_move_in is None:
            earliest_move_in = timezone.now()
        if latest_move_in is None:
            latest_move_in = timezone.now()
        if home_type is None:
            home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]

        survey = RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
            earliest_move_in=earliest_move_in,
            latest_move_in=latest_move_in,
            move_weight=move_weight,
            wants_laundry_in_building=wants_laundry_in_building,
            wants_laundry_in_unit=wants_laundry_in_unit,
            laundry_in_unit_weight=laundry_in_unit_weight,
            laundry_in_building_weight=laundry_in_building_weight,
            wants_update=wants_update,
            num_home_threshold=num_home_threshold,
            score_threshold=score_threshold,
            update_frequency=update_frequency,
            price_weight=price_weight,
        )
        # Add the home type
        survey.home_type.add(home_type)
        return survey

    def __str__(self):
        user_short_name = self.user_profile.user.get_short_name()
        survey_name = self.survey_name
        return "{0}: {1}".format(user_short_name, survey_name)


class TenantPersonalInformationModel(models.Model):
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    occupation = models.CharField(max_length=200, default="", blank=True)
    other_occupation_reason = models.CharField(max_length=200, default="", blank=True)
    unemployed_follow_up = models.CharField(max_length=200, default="", blank=True)
    income = models.IntegerField(default=-1, blank=True)
    credit_score = models.CharField(max_length=200, default="", blank=True)
    new_job = models.CharField(max_length=200, default="", blank=True)

    class Meta:
        abstract = True


class DestinationsModel(models.Model):
    street_address = models.CharField(max_length=200, default="", blank=True)
    city = models.CharField(max_length=200, default="", blank=True)
    state = models.CharField(max_length=200, default="", blank=True)
    zip_code = models.CharField(max_length=200, default="", blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    @property
    def full_address(self):
        if self.street_address == "" and self.city == "" and self.state == "" and self.zip_code == "":
            return ""
        else:
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
    max_commute = models.IntegerField(default=100)
    desired_commute = models.IntegerField(default=60)
    commute_weight = models.IntegerField(default=0)
    commute_type = models.ForeignKey(CommuteType)
    traffic_option = models.BooleanField(default=False)

    @property
    def min_commute(self):
        return 0

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
