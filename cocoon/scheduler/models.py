from django.db import models
from django.utils import timezone

# Import cocoon models
from cocoon.userAuth.models import MyUser
from cocoon.houseDatabase.models import RentDatabaseModel


class TimeModel(models.Model):
    """
        Model for a proposed itinerary start time.

        Attributes:
            self.time (DateTimeField) -> The available start time proposed by the client
            self.itinerary (ForeignKey) -> The associated itinerary
    """
    time = models.DateTimeField(default=timezone.now)
    itinerary = models.ForeignKey('ItineraryModel', related_name='start_times', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.time)


class ItineraryModel(models.Model):
    """
       Model for Itinerary. These are based on the interface designed on the Google Doc.

       Attributes:
           self.client: (ForeignKey('MyUser') -> The user that is associated with the itinerary
           self.itinerary: (FileField) -> The location of the itinerary stored on s3. Gives a step by step
                plan for the agent
           self.agent: (ForeignKey('MyUser') -> The agent that will be conducting the tour for the client
           self.tour_duration_seconds: (IntegerField) -> The tour duration stored in seconds
           self.selected_start_time (OneToOneField) -> Stores the selected time that the agent selected for the tour
           self.homes (ManytoManyField) -> Stores the homes that are associated with this itinerary
    """
    client = models.ForeignKey(MyUser, related_name='my_tours', on_delete=models.CASCADE)
    itinerary = models.FileField(blank=True)
    agent = models.ForeignKey(MyUser, related_name='scheduled_tours', on_delete=models.SET_NULL, blank=True, null=True)
    tour_duration_seconds = models.IntegerField(default=0)
    selected_start_time = models.OneToOneField('TimeModel', on_delete=models.SET_NULL, blank=True, null=True)
    homes = models.ManyToManyField(RentDatabaseModel, blank=True)

    def __str__(self):
        return "{0} Itinerary".format(self.client.full_name)

    @property
    def tour_duration_minutes(self):
        """
        Returns the tour duration in number of minutes
        """
        return self.tour_duration_seconds/60

    @property
    def tour_duration_hours(self):
        """
        Returns the tour duration in number of hours
        :return:
        """
        return self.tour_duration_minutes/60

    @property
    def is_claimed(self):
        """
        Returns if the itinerary has been claimed (has an agent)
        :return:
        """
        return self.agent != None

    @property
    def is_scheduled(self):
        """
        Returns if the itinerary has been schedueld (has a start time)
        :return:
        """
        return self.selected_start_time != None