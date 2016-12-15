from django.db import models
from userAuth.models import UserProfile
# Create your models here.


class InitialSurvey(models.Model):
    user = models.ForeignKey(UserProfile)
    survey_type = models.BooleanField()
    streetAddress = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
