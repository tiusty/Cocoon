from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import login, get_user
from django.utils import timezone

from cocoon.userAuth.models import MyUser, MyUserManager
from cocoon.scheduler.models import TimeModel, ItineraryModel
from cocoon.scheduler import views

def setup_test_itineraries(num_claimed=2, num_unclaimed=2):
    """
    Created scheduled and unscheduled itineraries for testing purposes

    :param num_claimed: number of claimed itineraries that will be created
    :param num_unclaimed: number of unclaimed itineraries that will be created

    :return:
        tuple containing list of claimed itineraries and list of unclaimed itineraries
    """
    agent = MyUser.objects.create(email="test@email.com", is_broker=True)
    client = MyUser.objects.create(email="client@email.com", is_hunter=True)
    claimed_itineraries = [ItineraryModel.objects.create(client=client, agent=agent) for i in range(num_claimed)]
    unclaimed_itineraries = [ItineraryModel.objects.create(client=client) for i in range(num_unclaimed)]
    return (claimed_itineraries, unclaimed_itineraries)

def get_hunter(email, password):
    hunter_user = MyUser.objects.create_user(email=email, password=password)
    hunter_user.is_hunter = True
    hunter_user.is_admin = False
    hunter_user.is_broker = False
    hunter_user.is_superuser = False
    hunter_user.save()
    return hunter_user

def get_broker(email, password):
    broker_user = MyUser.objects.create_user(email=email, password=password)
    broker_user.is_broker = True
    broker_user.is_admin = True
    broker_user.save()
    return broker_user

def get_admin(password):
    admin_user = MyUser.objects.create_superuser(email="admin@test.com", password=password)
    return admin_user

class AgentSchedulerViewTests(TestCase):
    """
    class for testing view methods of the scheduler
    """
    def setUp(self):
        self.password = "password"
        self.hunter_email = "hunter@email.com"
        self.broker_email = "broker@email.com"
        self.hunter = get_hunter(self.hunter_email, self.password)
        self.broker = get_broker(self.broker_email, self.password)
        self.admin = get_admin(self.password)

    def test_agent_scheduler(self):
        claimed_itineraries, unclaimed_itineraries = setup_test_itineraries()

        # should respond with redirect to logged out user
        response = self.client.get(reverse('scheduler:agentScheduler'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual("/userAuth/login" in response.url, True)

        # should respond with 404 to hunter
        self.client.login(username=self.hunter.email, password=self.password)
        self.assertEqual(get_user(self.client), self.hunter)
        response = self.client.get(reverse('scheduler:agentScheduler'))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        # should respond correctly to broker
        self.client.login(username=self.broker.email, password=self.password)
        self.assertEqual(get_user(self.client), self.broker)
        response = self.client.get(reverse('scheduler:agentScheduler'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(claimed_itineraries, [itn for itn in response.context['claimed_itineraries']])
        self.assertEqual(unclaimed_itineraries, [itn for itn in response.context['unclaimed_itineraries']])
        self.client.logout()

        # should respond correctly to admin
        self.client.login(username=self.admin.email, password=self.password)
        self.assertEqual(get_user(self.client), self.admin)
        response = self.client.get(reverse('scheduler:agentScheduler'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(claimed_itineraries, [itn for itn in response.context['claimed_itineraries']])
        self.assertEqual(unclaimed_itineraries, [itn for itn in response.context['unclaimed_itineraries']])
        self.client.logout()

    def test_scheduled_itinerary_views(self):
        # should respond with redirect to logged out user
        response = self.client.get(reverse('scheduler:myTours'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual("/userAuth/login" in response.url, True)

        # should respond with 404 to hunter
        self.client.login(username=self.hunter.email, password=self.password)
        self.assertEqual(get_user(self.client), self.hunter)
        response = self.client.get(reverse('scheduler:myTours'))
        request = response.wsgi_request
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        # setup scheduled itineraries for an agent
        scheduled_itineraries = []
        unscheduled_itineraries = []

        scheduled_itineraries = [ItineraryModel.objects.create(agent=self.broker, client=self.hunter, selected_start_time=timezone.now()) for i in range(3)]
        unscheduled_itineraries = [ItineraryModel.objects.create(agent=self.broker, client=self.hunter) for i in range(3)]

        self.client.login(username=self.broker.email, password=self.password)
        self.assertEqual(get_user(self.client), self.broker)
        response = self.client.get(reverse('scheduler:myTours'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(scheduled_itineraries, [itn for itn in response.context['scheduled_itineraries']])
        self.assertEqual(unscheduled_itineraries, [itn for itn in response.context['unscheduled_itineraries']])
        self.client.logout()

    def test_uschedule_itinerary(self):

        # user can succesfully unschedule an itinerary of theirs
        scheduled_itinerary = ItineraryModel.objects.create(agent=self.broker, client=self.hunter, selected_start_time=timezone.now())
        self.assertIsNot(scheduled_itinerary.selected_start_time, None)
        self.client.login(username=self.hunter.email, password=self.password)
        self.assertEqual(get_user(self.client), self.hunter)
        self.client.post(reverse('scheduler:unscheduleItinerary'), {'itinerary_id': scheduled_itinerary.id})
        self.assertEqual(ItineraryModel.objects.get(id=scheduled_itinerary.id).selected_start_time, None)
        self.client.logout()

        # user cannot unschedule another user's itinerary
        scheduled_itinerary = ItineraryModel.objects.create(agent=self.broker, client=self.hunter, selected_start_time=timezone.now())
        alt_user = get_hunter("hunter2@email.com", self.password)
        self.client.login(username=alt_user.email, password=self.password)
        self.assertEqual(get_user(self.client), alt_user)
        response = self.client.post(reverse('scheduler:unscheduleItinerary'), {'itinerary_id': scheduled_itinerary.id})
        self.assertIsNot(ItineraryModel.objects.get(id=scheduled_itinerary.id).selected_start_time, None)
        self.client.logout()

    def test_claim_itinerary(self):

        # agent can claim an itinerary
        unclaimed_itinerary = ItineraryModel.objects.create(client=self.hunter)
        self.assertIs(unclaimed_itinerary.agent, None)

        self.client.login(username=self.broker.email, password=self.password)
        self.assertEqual(get_user(self.client), self.broker)
        response = self.client.post(reverse('scheduler:claimItinerary'), {'itinerary_id': unclaimed_itinerary.id})
        self.assertIs(ItineraryModel.objects.get(id=unclaimed_itinerary.id).agent.id, self.broker.id)
        self.client.logout()

        # agent cannot claim a claimed itinerary
        alt_agent = get_broker("broker2@email.com", self.password)
        self.client.login(username=alt_agent.email, password=self.password)
        self.assertEqual(get_user(self.client), alt_agent)
        response = self.client.post(reverse('scheduler:claimItinerary'), {'itinerary_id': unclaimed_itinerary.id})
        self.assertIs(ItineraryModel.objects.get(id=unclaimed_itinerary.id).agent.id, self.broker.id)
        self.client.logout()

    def test_select_start_time(self):

        # agent can select an itinerary
        claimed_itinerary = ItineraryModel.objects.create(agent=self.broker, client=self.hunter)
        available_time = TimeModel.objects.create(itinerary=claimed_itinerary)
        self.client.login(username=self.broker.email, password=self.password)
        self.assertEqual(get_user(self.client), self.broker)
        response = self.client.post(reverse('scheduler:selectStartTime'), {
            'itinerary_id': claimed_itinerary.id,
            'time_id': available_time.id
        })
        self.assertEqual(ItineraryModel.objects.get(id=claimed_itinerary.id).selected_start_time, available_time.time)
        self.client.logout()