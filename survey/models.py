from django.db import models
from userAuth.models import UserProfile

import math
from django.utils import timezone

# Import Global Variables
from Unicorn.settings.Global_Config import Max_Num_Bathrooms, default_rent_survey_name, \
    default_buy_survey_name


class InitialSurveyModel(models.Model):
    """
    Stores the default information across all the surveys
    Stores survey type and when it was created
    """
    survey_type = models.IntegerField(default=-1)
    created = models.DateField(auto_now_add=True)


class HomeType(models.Model):
    """
    Class stores all the different homes types
    This generates the multiple select field in the survey
    If another home gets added it needs to be added here in the HOME_TYPE
    tuples but also allowed past the query in the survey result view.
    """
    HOME_TYPE = (
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('town_house', 'Town House'),
    )
    homeType = models.CharField(
        choices=HOME_TYPE,
        max_length=200,
    )

    def __str__(self):
        return self.homeType


class InteriorAmenities(models.Model):
    """
    Contains all the survey questions regarding the interior amenities
    Any survey can inherit these fields
    """
    air_conditioning = models.IntegerField(default=0)
    wash_dryer_in_home = models.IntegerField(default=0)
    dish_washer = models.IntegerField(default=0)
    bath = models.IntegerField(default=0)
    max_bathrooms = models.IntegerField(default=Max_Num_Bathrooms)
    min_bathrooms = models.IntegerField(default=0)

    def get_air_conditioning(self):
        return self.air_conditioning

    def get_wash_dryer_in_home(self):
        return self.wash_dryer_in_home

    def get_dish_washer(self):
        return self.dish_washer

    def get_bath(self):
        return self.bath

    def get_max_bathrooms(self):
        return self.max_bathrooms

    def get_min_bathrooms(self):
        return self.min_bathrooms

    class Meta:
        abstract = True


class BuildingExteriorAmenities(models.Model):
    """
    Contains all the survey questions regarding the building/Exterior Amenities
    Any survey can inherit these fields
    All Questions are hybrid weighted
    """
    parking_spot = models.IntegerField(default=0)
    washer_dryer_in_building = models.IntegerField(default=0)
    elevator = models.IntegerField(default=0)
    handicap_access = models.IntegerField(default=0)
    pool_hot_tub = models.IntegerField(default=0)
    fitness_center = models.IntegerField(default=0)
    storage_unit = models.IntegerField(default=0)

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

    class Meta:
        abstract = True


class RequiredInformation(models.Model):
    name = models.CharField(max_length=200, default=default_rent_survey_name)
    max_price = models.IntegerField(default=0)
    min_price = models.IntegerField(default=0)
    price_weight = models.IntegerField(default=0)
    max_commute = models.IntegerField(default=0)
    min_commute = models.IntegerField(default=0)
    commute_weight = models.IntegerField(default=1)
    move_in_date_start = models.DateField(default=timezone.now)
    move_in_date_end = models.DateField(default=timezone.now)
    num_bedrooms = models.IntegerField(default=0)
    home_type = models.ManyToManyField(HomeType)

    def get_name(self):
        return self.name

    def get_max_price(self):
        return self.max_price

    def get_min_price(self):
        return self.min_price

    def get_price_weight(self):
        return self.price_weight

    def get_max_commute(self):
        return self.max_commute

    def get_min_commute(self):
        return self.min_commute

    def get_commute_weight(self):
        return self.commute_weight

    def get_move_in_date_start(self):
        return self.move_in_date_start

    def get_move_in_date_end(self):
        return self.move_in_date_end

    def get_num_bedrooms(self):
        return self.num_bedrooms

    class Meta:
        abstract = True


class RentingSurveyModel(InitialSurveyModel, RequiredInformation, InteriorAmenities, BuildingExteriorAmenities):
    """
    Renting Survey Model is the model for storing data from the renting survey model.
    It takes the Initial Survey model as an input which is data that is true for all surveys
    The user may take multiple surveys and it is linked to their User Profile

    Default name is stored unless the User changes it. Everytime a survey is created the past
    default name is deleted to allow for the new one. Therefore, there is always a history
    of one survey
    """
    userProf = models.ForeignKey(UserProfile)

    def get_short_name(self):
        user_short_name = self.userProf.user.get_short_name()
        survey_name = self.get_name()
        output = user_short_name + ": " + survey_name
        return output

    def __str__(self):
        user_short_name = self.userProf.user.get_short_name()
        survey_name = self.get_name()
        output = user_short_name + ": " + survey_name
        return output

    def get_cost_range(self):
        if self.get_max_price() == 0:
            return "Not set"
        else:
            price_output = "$" + str(self.get_min_price()) + " - $" + str(self.get_max_price())
            return price_output

    def get_commute_range(self):
        if self.get_max_commute() == 0:
            return "Not Set"
        else:
            if self.get_max_commute() > 60:
                max_output = str(math.floor(self.get_max_commute()/60)) + " hours " + str(self.get_max_commute() % 60) \
                             + " Minutes"
            else:
                max_output = str(self.get_max_commute()) + " Minutes"
            if self.get_min_commute() > 60:
                min_output = str(math.floor(self.get_min_commute()/60)) + " hours " + str(self.get_min_commute() % 60) \
                             + " Minutes"
            else:
                min_output = str(self.get_min_commute()) + " Minutes"

        return min_output + " - " + max_output

    def get_home_types(self):
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


# Default name for buying survey
class BuyingSurveyModel(InitialSurveyModel):
    name = models.CharField(max_length=200, default=default_buy_survey_name)
    maxPrice = models.IntegerField(default=0)


# Stores the destination address since there can be multiple
class Destinations(models.Model):
    streetAddress = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)

    def full_address(self):
        output = str(self.streetAddress) + ", " + str(self.city) + ", " + str(self.state) + ", " + str(self.zip_code)
        return output


# Used for the renting survey
class RentingDestinations(Destinations):
    survey = models.ForeignKey(RentingSurveyModel)

    def __str__(self):
        return self.streetAddress

    def full_address(self):
        return self.streetAddress + ", " + self.city + ", " + self.state + " " + self.zip_code

    def short_address(self):
        return self.streetAddress + ", " + self.city


class BuyingDestinations(Destinations):
    survey = models.ForeignKey(BuyingSurveyModel)
