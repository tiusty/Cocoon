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
    airConditioning = models.IntegerField(default=0)
    washDryer_InHome = models.IntegerField(default=0)
    dishWasher = models.IntegerField(default=0)
    bath = models.IntegerField(default=0)
    maxBathrooms = models.IntegerField(default=Max_Num_Bathrooms)
    minBathrooms = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BuildingExteriorAmenities(models.Model):
    """
    Contains all the survey questions regarding the building/Exterior Amenities
    Any survey can inherit these fields
    All Questions are hybrid weighted
    """
    parkingSpot = models.IntegerField(default=0)
    washerDryer_inBuilding = models.IntegerField(default=0)
    elevator = models.IntegerField(default=0)
    handicapAccess = models.IntegerField(default=0)
    poolHottub = models.IntegerField(default=0)
    fitnessCenter = models.IntegerField(default=0)
    storageUnit = models.IntegerField(default=0)

    class Meta:
        abstract = True


class RequiredInformation(models.Model):
    name = models.CharField(max_length=200, default=default_rent_survey_name)
    maxPrice = models.IntegerField(default=0)
    minPrice = models.IntegerField(default=0)
    price_weight = models.IntegerField(default=0)
    maxCommute = models.IntegerField(default=0)
    minCommute = models.IntegerField(default=0)
    commuteWeight = models.IntegerField(default=1)
    moveinDateStart = models.DateField(default=timezone.now)
    moveinDateEnd = models.DateField(default=timezone.now)

    numBedrooms = models.IntegerField(default=0)
    home_type = models.ManyToManyField(HomeType)

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
        survey_name = self.name
        output = user_short_name + ": " + survey_name
        return output

    def __str__(self):
        user_short_name = self.userProf.user.get_short_name()
        survey_name = self.name
        output = user_short_name + ": " + survey_name
        return output

    def get_cost_range(self):
        if self.maxPrice == 0:
            return "Not set"
        else:
            price_output = "$" + str(self.minPrice) + " - $" + str(self.maxPrice)
            return price_output

    def get_commute_range(self):
        if self.maxCommute == 0:
            return "Not Set"
        else:
            if self.maxCommute > 60:
                max_output = str(math.floor(self.maxCommute/60)) + " hours " + str(self.maxCommute % 60) + " Minutes"
            else:
                max_output = str(self.maxCommute) + " Minutes"
            if self.minCommute > 60:
                min_output = str(math.floor(self.minCommute/60)) + " hours " + str(self.minCommute % 60) + " Minutes"
            else:
                min_output = str(self.minCommute) + " Minutes"

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
class RentingDesintations(Destinations):
    survey = models.ForeignKey(RentingSurveyModel)

    def __str__(self):
        return self.streetAddress

    def full_address(self):
        return self.streetAddress + ", " + self.city + ", " + self.state + " " + self.zip_code

    def short_address(self):
        return self.streetAddress + ", " + self.city


class BuyingDestinations(Destinations):
    survey = models.ForeignKey(BuyingSurveyModel)
