# Django modules
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse

# Models
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.userAuth.models import UserProfile
from cocoon.scheduler.models import ItineraryModel

# Python Modules
import json

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
        raise Http404("This page does not exist")
    return render(request, 'scheduler/itineraryPicker.html', context)

@login_required()
def view_tours(request):
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if current_profile.user.is_broker or current_profile.user.is_admin:
        context = {}
        unscheduled_itineraries = ItineraryModel.objects.filter(agent=current_profile.user, selected_start_time=None)
        scheduled_itineraries = ItineraryModel.objects.fillter(agent=current_profile.user).exclude(selected_start_time=None)
        context['unscheduled_itineraries'] = unscheduled_itineraries
        context['scheduled_itineraries'] = scheduled_itineraries
    else:
        raise Http404("This page does not exist")
    return render(request, 'scheduler/viewTours.html', context)


########################################
# AJAX Request Handlers
########################################

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
                            itinerary.agent = current_profile.user
                            itinerary.save()
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
                    return HttpResponse(json.dumps({"result: User does not have priviledges"},
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
                    itinerary_id = request.POST.get('itinerary_id')
                    try:
                        itinerary = ItineraryModel.objects.get(id=itinerary_id)
                        if itinerary.agent is None:
                            itinerary.agent = current_profile.user
                            itinerary.save()
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
                    return HttpResponse(json.dumps({"result: User does not have priviledges"},
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

