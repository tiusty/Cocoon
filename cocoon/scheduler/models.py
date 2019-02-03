# Import django modules
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

# Import cocoon models
from cocoon.userAuth.models import MyUser
from cocoon.houseDatabase.models import RentDatabaseModel

# Import third party libraries
import hashlib
import pytz


def itinerary_directory_path(instance, filename):
    return "itinerary/{0}/{1}".format(instance.client.id, str(instance.id) + "_" + filename)


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
    itinerary = models.FileField(blank=True, upload_to=itinerary_directory_path)
    agent = models.ForeignKey(MyUser, related_name='scheduled_tours', on_delete=models.SET_NULL, blank=True, null=True)
    tour_duration_seconds = models.IntegerField(default=0)
    selected_start_time = models.DateTimeField(default=None, blank=True, null=True)
    homes = models.ManyToManyField(RentDatabaseModel, blank=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return "{0} Itinerary".format(self.client.full_name)

    @property
    def hash(self):
        """
        Hashes all the values associated with the itinerary so if any of the data fields changes values,
            the hash changes values. This will determine that the itinerary has been updated
        :return:  (string) -> The hex form of the hash
        """

        # Get all the homes and store the ids
        home_ids = ""
        for home in self.homes.all():
            home_ids = home_ids + str(home.id)

        # Get all the start times and add their ids
        start_time_ids = ""
        for time in self.start_times.all():
            start_time_ids = start_time_ids + str(time.id)

        selected_start_time = "null"
        if self.selected_start_time is not None:
            selected_start_time = self.selected_start_time

        client_id = "null"
        if self.client is not None:
            client_id = self.client.id

        agent_id = "null"
        if self.agent is not None:
            agent_id = self.agent.id

        # Now create a string that will be hashed. It should contain all the data from the
        #   itinerary model
        hashable_string = "{0}{1}{2}{3}{4}{5}{6}".format(client_id,
                                                         agent_id,
                                                         self.tour_duration_seconds,
                                                         selected_start_time,
                                                         start_time_ids,
                                                         home_ids,
                                                         self.finished)

        # Create the md5 object
        m = hashlib.md5()

        # Adds the string to the hash function
        m.update(hashable_string.encode('utf-8'))

        # Returns the hash as hex
        return m.hexdigest()

    @property
    def tour_duration_seconds_rounded(self):
        """
        Returns the tour duration in number of seconds rounded up to the nearest 15 minutes
        :return:
        """
        # Determines how many seconds over the nearest 15 minutes the tour is
        sec_over = self.tour_duration_seconds % (15 * 60)
        # Subtracts out the seconds over and then add 900 which rounds unless the number of seconds
        #   already equaled
        if sec_over is 0:
            return self.tour_duration_seconds
        else:
            return self.tour_duration_seconds - sec_over + (15 * 60)

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
    def is_pending(self):
        """
        Returns if the itinerary has available start times or not. If it does not have available start times then it is
            pending user input
        :return: (boolean) -> True: The itinerary still is awaiting for the client to enter available start times
                              False: The client added available start times
        """
        return self.start_times.count() == 0

    @property
    def is_claimed(self):
        """
        Returns if the itinerary has been claimed (has an agent)
        :return:
            True if the itinerary is claimed (associated with an agent)
            False otherwise (available for an agent to claim)
        """
        return self.agent is not None

    @property
    def is_scheduled(self):
        """
        Returns if the itinerary has been scheduled (has a selected start time)
        :return: (boolean) -> True: A start time has been selected for the tour
                              False: A start time has not been selected for the tour
        """
        return self.selected_start_time is not None

    @staticmethod
    def retrieve_unfinished_itinerary(user):
        return ItineraryModel.objects.filter(client=user).filter(finished=False)

    @transaction.atomic
    def select_start_time(self, start_time):
        self.selected_start_time = start_time
        self.save()

        eastern_datetime = timezone.localtime(self.selected_start_time, pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
        message = render_to_string(
            'scheduler/email/itinerary_confirmation_email.html',
            {
                'user': self.client.first_name,
                'agent_name': self.agent.first_name,
                'agent_email': self.agent.email,
                'start_time': eastern_datetime,
                'homes': self.homes,
            }
        )
        subject = 'Tour confirmed for {0}'.format(eastern_datetime)
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
                'start_time': timezone.localtime(unscheduled_time, pytz.timezone('US/Eastern')),
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


class TimeModel(models.Model):
    """
        Model for a proposed itinerary start time.

        Attributes:
            self.time (DateTimeField) -> The available start time proposed by the client
            self.itinerary (ForeignKey) -> The associated itinerary
    """
    time = models.DateTimeField(default=timezone.now)
    itinerary = models.ForeignKey(ItineraryModel, related_name='start_times', on_delete=models.CASCADE, blank=False, null=False)
    time_available_seconds = models.IntegerField(default=0)

    def __str__(self):
        return str(self.time)
