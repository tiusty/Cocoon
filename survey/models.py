from django.db import models
from userAuth.models import UserProfile
from enum import Enum
# Create your models here.

survey_types = Enum('survey_type','rent buy')


class InitialSurveyModel(models.Model):
    user = models.ForeignKey(UserProfile)
    survey_type = models.IntegerField(default=-1)
    streetAddress = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)


class RentingSurveyModel(InitialSurveyModel):
    name = models.CharField(max_length=200)

