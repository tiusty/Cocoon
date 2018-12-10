# Django modules
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

# Models
from cocoon.userAuth.models import UserProfile
from cocoon.scheduler.models import ItineraryModel, TimeModel
from .serializers import ItinerarySerializer

# Python Modules
import json

# Rest Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response


class ClientScheduler(TemplateView):
    """
    Loads the template for the ClientScheduler

    The template has the entry point for React and react handles
        the rest of the frontend
    """
    template_name = 'scheduler/clientScheduler.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Tells React which component to load onto the page
        data['component'] = ClientScheduler.__name__
        return data


class AgentSchedulerPortal(TemplateView):
    """
    Loads the template for the AgentSchedulerPortal

    The template contains the entry point for React and react handles
    retrieving the necessary data
    """
    template_name = 'scheduler/agentSchedulerPortal.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Tells React which component to load onto the page
        data['component'] = AgentSchedulerPortal.__name__
        return data


class AgentSchedulerMarketplace(TemplateView):
    """
        Loads the template for the AgentSchedulerMarketplace

        The template contains the entry point for React and react handles
        retrieving the necessary data
        """
    template_name = 'scheduler/agentSchedulerMarketplace.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Tells React which component to load onto the page
        data['component'] = AgentSchedulerMarketplace.__name__
        return data


@method_decorator(user_passes_test(lambda u: u.is_hunter or u.is_admin), name='dispatch')
class ItineraryClientViewSet(viewsets.ModelViewSet):

    serializer_class = ItinerarySerializer

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        print(user_profile)
        return ItineraryModel.objects.filter(client=user_profile.user)


@method_decorator(user_passes_test(lambda u: u.is_broker or u.is_admin), name='dispatch')
class ItineraryAgentViewSet(viewsets.ModelViewSet):

    serializer_class = ItinerarySerializer

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        itinerary_type = self.request.query_params.get('type', None)

        if itinerary_type == 'unscheduled':
            return ItineraryModel.objects.filter(agent=user_profile.user, selected_start_time=None)\
                .exclude(finished=True)
        elif itinerary_type == 'scheduled':
            return ItineraryModel.objects.filter(agent=user_profile.user).exclude(selected_start_time=None)\
                .exclude(finished=True)

    def update(self, request, *args, **kwargs):

        result = False
        reason = ''

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the itinerary id
        pk = kwargs.pop('pk', None)

        # Retrieve the associated itinerary with the request
        itinerary = get_object_or_404(ItineraryModel, pk=pk)

        # Case if an agent is trying to schedule an itinerary they already claimed
        if 'schedule' in self.request.data['type']:
            time_id = self.request.data['time_id']

            # The start time must be one of the available start times for that itinerary
            try:
                time = TimeModel.objects.filter(itinerary=itinerary).get(id=time_id)
                itinerary.select_start_time(time.time)
                result = True
            except TimeModel.DoesNotExist:
                result = False
                reason = 'Start time is not one of the available start times'

        # Case if the agent is trying to claim an itinerary from the market
        elif 'claim' in self.request.data['type']:

            # If the itinerary is already claimed then the agent cannot claim it anymore
            if itinerary.agent is None:
                itinerary.associate_agent(user_profile.user)
                result = True
            else:
                result = False
                reason = 'Itinerary already claimed'

        return Response({'result': result,
                         'reason': reason})

    # allows agents to retrieve specific client itineraries
    def retrieve(self, request, *args, **kwargs):
        # Retrieve the itinerary id
        pk = kwargs.pop('pk', None)
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        queryset = ItineraryModel.objects.filter(agent=user_profile.user)
        client_itinerary = get_object_or_404(queryset, pk=pk)
        serializer = ItinerarySerializer(client_itinerary)
        return Response(serializer.data)


@method_decorator(user_passes_test(lambda u: u.is_broker or u.is_admin), name='dispatch')
class ItineraryMarketViewSet(viewsets.ModelViewSet):

    serializer_class = ItinerarySerializer

    def get_queryset(self):

        return ItineraryModel.objects.filter(agent=None).exclude(finished=True)


########################################
# AJAX Request Handlers
########################################

@login_required
def unschedule_itinerary(request):
    itinerary_id = request.POST.get('itinerary_id')
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if current_profile.user.is_hunter:
        try:
            itinerary = ItineraryModel.objects.get(id=itinerary_id)
            if itinerary.client.id != current_profile.user.id:
                return HttpResponse(json.dumps({"result": "1"}),
                                    content_type="application/json")
            itinerary.unschedule_itinerary(request=request)
            return HttpResponse(json.dumps({"result": "0"}),
                                content_type="application/json",
                                )
        except ItineraryModel.DoesNotExist:
            return HttpResponse(json.dumps({"result": "1"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "1"}),
                            content_type="application/json",
                            )
@login_required
def select_start_time(request):
    """
    This ajax function selects a start time for an agent
    :param request: Http request
    :return:
        0 -> succes, itinerary was claimed
        1 -> itinerary was already claimed
    """

    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            try:
                current_profile = get_object_or_404(UserProfile, user=request.user)
                if current_profile.user.is_broker or current_profile.user.is_admin:
                    time_id = request.POST.get('time_id')
                    itinerary_id = request.POST.get('itinerary_id')
                    try:
                        time = TimeModel.objects.get(id=time_id)
                        itinerary = ItineraryModel.objects.get(id=itinerary_id)
                        if (itinerary.agent == current_profile.user) and (itinerary.selected_start_time is None):
                            itinerary.select_start_time(time.time)

                            return HttpResponse(json.dumps({"result": "0",
                                                            "timeId": time.id,
                                                            }), content_type="application/json")
                        else:
                            return HttpResponse(json.dumps({"result": "1"}),
                                                content_type="application/json")
                    except (ItineraryModel.DoesNotExist, TimeModel.DoesNotExist):
                        return HttpResponse(json.dumps({"result": "Could not find itinerary data"}),
                                            content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"result: User does not have pri1vileges"},
                                                    content_type="application/json"))
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "Method Not POST"}),
                            content_type="application/json",
                            )

