from django.db import models
from userAuth.models import UserProfile
from enum import Enum
import math
# Create your models here.

survey_types = Enum('survey_types', 'rent buy')


# Stores the type of home
class InitialSurveyModel(models.Model):
    survey_type = models.IntegerField(default=-1)
    created = models.DateField(auto_now_add=True)


class HomeType(models.Model):
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

# Default name for rent survey that is used for the last survey created
# Every user gets a history of one survey
default_rent_survey_name = "Recent Rent Survey"
maxCommuteTime = 180
class RentingSurveyModel(InitialSurveyModel):
    userProf = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=200, default=default_rent_survey_name)
    maxPrice = models.IntegerField(default=0)
    minPrice = models.IntegerField(default=0)
    maxCommute = models.IntegerField(default=0)
    minCommute = models.IntegerField(default=0)
    home_type = models.ManyToManyField(HomeType)

    def get_short_name(self):
        nameProf = self.userProf.user.get_short_name()
        nameSurvey = self.name
        output = nameProf + ": " + nameSurvey
        return output

    def __str__(self):
        nameProf = self.userProf.user.get_short_name()
        nameSurvey = self.name
        output = nameProf + ": " + nameSurvey
        return output

    def get_cost_range(self):
        if self.maxPrice == 0:
            return "Not set"
        else:
            priceOutput = "$" + str(self.minPrice) + " - $" + str(self.maxPrice)
            return priceOutput

    def get_commute_range(self):
        if self.maxCommute == 0:
            return "Not Set"
        else:
            if self.maxCommute > 60:
                maxOutput = str(math.floor(self.maxCommute/60)) + " hours " + str(self.maxCommute%60) + " Minutes"
            else:
                maxOutput = str(self.maxCommute) + " Minutes"
            if self.minCommute > 60:
                minOutput = str(math.floor(self.minCommute/60)) + " hours " + str(self.minCommute%60) + " Minutes"
            else:
                minOutput = str(self.minCommute) + " Minutes"

        return minOutput + " - " + maxOutput

    def get_home_types(self):
        homeTypeSet = self.home_type.all()
        if homeTypeSet.count() == 0:
            return "Not set"
        else:
            typeOutput = ""
            counter = 0
            for homeType in homeTypeSet:
                if counter == 0:
                    typeOutput = str(homeType)
                    counter = counter + 1
                else:
                    typeOutput = str(homeType) + ", " + typeOutput

        return typeOutput


# Default name for buying survey
default_buy_survey_name = "recent_buy_survey"
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




