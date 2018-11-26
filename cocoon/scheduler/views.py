# Django modules
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.db import models
from django.views.generic import TemplateView

# Models
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.userAuth.models import UserProfile
from cocoon.scheduler.models import ItineraryModel, TimeModel

# Python Modules
import json


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


@login_required()
def agent_scheduler(request):
    context = {}
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if current_profile.user.is_broker or current_profile.user.is_admin:
        unclaimed_itineraries = ItineraryModel.objects.filter(agent=None)
        claimed_itineraries = ItineraryModel.objects\
            .filter(selected_start_time=None)\
            .exclude(agent=None)
        context['unclaimed_itineraries'] = unclaimed_itineraries
        context['claimed_itineraries'] = claimed_itineraries

    else:
        return HttpResponseNotFound()
    return render(request, 'scheduler/itineraryPicker.html', context)

@login_required()
def view_tours(request):
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if current_profile.user.is_broker or current_profile.user.is_admin:
        context = {}
        unscheduled_itineraries = ItineraryModel.objects.filter(agent=current_profile.user, selected_start_time=None)
        scheduled_itineraries = ItineraryModel.objects.filter(agent=current_profile.user).exclude(selected_start_time=None)
        context['unscheduled_itineraries'] = unscheduled_itineraries
        context['scheduled_itineraries'] = scheduled_itineraries
    else:
        return HttpResponseNotFound()
    return render(request, 'scheduler/viewTours.html', context)

@login_required
def get_user_itineraries(request):
    """
    A helper function intended for use in other views to add the
    given user's itineraries to the current context
    :param request: The current http request
    :return: The context containing the user's itineraries
    """
    if request.user.is_authenticated():
        user_profile = get_object_or_404(UserProfile, user=request.user)
        itineraries = ItineraryModel.objects.filter(client=user_profile.user)
        unscheduled_itineraries = itineraries.filter(selected_start_time=None)
        scheduled_itineraries = itineraries.exclude(selected_start_time=None)
        return {
            'unscheduled_itineraries': unscheduled_itineraries,
            'scheduled_itineraries': scheduled_itineraries,
        }
    else:
        return {
            'scheduled_itineraries': None,
            'unscheduled_itineraries': None,
        }


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
def claim_itinerary(request):
    """
    This ajax function associates an agent to an itinerary
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
                    itinerary_id = request.POST.get('itinerary_id')
                    try:
                        itinerary = ItineraryModel.objects.get(id=itinerary_id)
                        if itinerary.agent is None:
                            itinerary.associate_agent(current_profile.user)
                            return HttpResponse(json.dumps({"result": "0",
                                                            "itineraryId": itinerary_id,
                                                            }), content_type="application/json")
                        else:
                            return HttpResponse(json.dumps({"result": "1"}),
                                                content_type="application/json")
                    except ItineraryModel.DoesNotExist:
                        return HttpResponse(json.dumps({"result": "Could not find itinerary"}),
                                            content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"result: User does not have privileges"},
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

