from cocoon.userAuth.models import UserProfile
from cocoon.scheduler.models import ItineraryModel, TimeModel

from django.shortcuts import get_object_or_404


def determine_user_type_processor(request):
    """
    This context processor adds whether or not the user is a broker or hunter to all pages
    :param request: The current http request
    :return: Adds the context of if they are a broker or not if the user is authenticated
    """
    if request.user.is_authenticated():
        user_profile = get_object_or_404(UserProfile, user=request.user)
        is_broker = user_profile.user.is_broker
        is_hunter = user_profile.user.is_hunter
        return {
            'is_broker': is_broker,
            'is_hunter': is_hunter,
        }
    return {}


