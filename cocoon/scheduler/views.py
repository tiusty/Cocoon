# Django modules
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404

# Models
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.userAuth.models import UserProfile
from cocoon.scheduler.models import ItineraryModel

@login_required()
def agent_scheduler(request):
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if current_profile.user.is_broker or current_profile.user.is_admin:
        available_itineraries = ItineraryModel.objects.filter(agent=None)
        context = {'itineraries': available_itineraries}
    else:
        raise Http404("This page does not exist")
    return render(request, 'scheduler/itineraryPicker.html', context)
