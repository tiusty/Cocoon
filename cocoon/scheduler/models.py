# import python modules
from datetime import datetime

from django.db import models
from django.db import transaction
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

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
           self.tour_duration_seconds: (IntegerField) -> The tour duration stored in seconds
           self.selected_start_time (OneToOneField) -> Stores the selected time that the agent selected for the tour
           self.homes (ManytoManyField) -> Stores the homes that are associated with this itinerary
    """
    client = models.ForeignKey(MyUser, related_name='my_tours', on_delete=models.CASCADE)
    itinerary = models.FileField(blank=True)
    agent = models.ForeignKey(MyUser, related_name='scheduled_tours', on_delete=models.SET_NULL, blank=True, null=True)
    tour_duration_seconds = models.IntegerField(default=0)
    selected_start_time = models.DateTimeField(default=None, blank=True, null=True)
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
            True if the itinerary is claimed (associated with an agent)
            False otherwise (available for an agent to claim)
        """
        return self.agent != None

    @property
    def is_scheduled(self):
        """
        Returns if the itinerary has been schedueld (has a start time)
        :return:
        """
        return self.selected_start_time != None

    @transaction.atomic
    def select_start_time(self, start_time):
        self.selected_start_time = start_time
        self.save()

        message = render_to_string(
            'scheduler/email/itinerary_confirmation_email.html',
            {
                'user': self.client.first_name,
                'agent_name': self.agent.first_name,
                'agent_email': self.agent.email,
                'start_time': self.selected_start_time,
                'homes': self.homes,
            }
        )
        subject = 'Tour confirmed for %s'%(str(self.selected_start_time))
        recipient = self.client.email
        email = EmailMessage(
            subject=subject, body=message, to=[recipient]
        )
        email.content_subtype = "html"

        # send confirmation email to user
        email.send()

    @transaction.atomic
    def associate_agent(self, agent):
        self.agent = agent
        self.save()

    @transaction.atomic
    def unschedule_itinerary(self, **kwargs):
        """
        Removes the selected start time from an itinerary and emails the
        relevant agent. Note that the associated agent is not removed
        from the itinerary (it is still claimed)

        :param kwargs:
            request - the request passed down from the view function that
            called this method - for retrieving the absolute url
        """
        unscheduled_time = self.selected_start_time
        unscheduled_available_time = self.start_times.filter(time=unscheduled_time).first()
        if unscheduled_available_time:
            unscheduled_available_time.delete()
        self.selected_start_time = None
        self.save()

        domain = kwargs.pop('request', None)
        current_site = get_current_site(domain)
        message = render_to_string(
            'scheduler/email/itinerary_cancellation_email.html',
            {
                'user': self.client.first_name,
                'agent_name': self.agent.first_name,
                'domain': current_site.domain,
                'agent_email': self.agent.email,
                'start_time': unscheduled_time,
            }
        )
        subject = 'Tour with %s cancelled' % (str(self.client.first_name))
        recipient = self.agent.email
        email = EmailMessage(
            subject=subject, body=message, to=[recipient]
        )
        email.content_subtype = "html"

        # send confirmation email to user
        email.send()
        
def itinerary_directory_path(user):
    return "itinerary_route_" + str(user) + "_" + str(datetime.now())

class TimeModel(models.Model):
    """
        Model for a proposed itinerary start time.

        Attributes:
            self.time (DateTimeField) -> The available start time proposed by the client
            self.itinerary (ForeignKey) -> The associated itinerary
    """
    time = models.DateTimeField(default=timezone.now)
    itinerary = models.ForeignKey(ItineraryModel, related_name='start_times', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.time)
