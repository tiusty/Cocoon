from django.db import models
from userAuth.models import UserProfile
from enum import Enum
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.

survey_types = Enum('survey_types', 'rent buy')

# Stores the type of home


class InitialSurveyModel(models.Model):
    userProf = models.ForeignKey(UserProfile)
    survey_type = models.IntegerField(default=-1)
    streetAddress = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)


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
default_rent_survey_name = "recent_rent_survey"
class RentingSurveyModel(InitialSurveyModel):
    name = models.CharField(max_length=200, default=default_rent_survey_name)
    amountMaxCommuteLow = models.IntegerField(default=0)
    amountMaxCommuteHigh = models.IntegerField(default=0)
    home_type = models.ManyToManyField(HomeType)

    def get_short_name(self):
        nameProf = self.userProf.user.get_short_name()
        nameSurvey = self.name
        output = nameProf + ": " + nameSurvey
        return output

    def __str__(self):
        nameProf = self.userProf.user.get_short_name()
        nameSurvey = self.name
        output = nameProf + ": "+ nameSurvey
        return output

# Default name for buying survey
default_buy_survey_name = "recent_buy_survey"
class BuyingSurveyModel(InitialSurveyModel):
    name = models.CharField(max_length=200, default=default_buy_survey_name)







