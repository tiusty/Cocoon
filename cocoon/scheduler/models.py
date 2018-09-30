from django.db import models
from django.utils import timezone

# Import cocoon models
from cocoon.userAuth.models import MyUser
from cocoon.houseDatabase.models import RentDatabaseModel


class ItineraryModel(models.Model):
    """
       Model for Itinerary. These are based on the interface designed on the Google Doc.

       Attributes:
           self.client: (ForeignKey('MyUser') -> The user that is associated with the itinerary
           self.itinerary: (FileField) -> The location of the itinerary stored on s3. Gives a step by step
                plan for the agent
           self.agent: (ForeignKey('MyUser') -> The agent that will be conducting the tour for the client
           self.estimated_tour_duration: (IntegerField) -> The tour duration stored in seconds
           self.selected_start_time
    """
    client = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    itinerary = models.FileField(blank=True)
    agent = models.ForeignKey('MyUser', on_delete=models.CASCADE, blank=True)
    estimated_tour_duration = models.IntegerField(default=0)
    selected_start_time = models.OneToOneField('TimeModel', on_delete=models.CASCADE, blank=True)
    available_start_times = models.ForeignKey('TimeModel', on_delete=models.CASCADE, blank=True)
    homes = models.ManyToManyField(RentDatabaseModel, blank=True)

    def __str__(self):
        return "{0} Itinerary".format(self.client.full_name)


class TimeModel(models.Model):
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.time
