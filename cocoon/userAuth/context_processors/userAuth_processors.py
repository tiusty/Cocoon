from cocoon.userAuth.models import UserProfile

from django.shortcuts import get_object_or_404


def add_favorite_homes_processor(request):
    """
    This context Processor adds all the users favorited home to the content of the page.
    Therefore, the page has a list of every home that the user favorited
    :param request: The current http request
    :return: The new context variable which contains a list of all the homes that the user favorited
    """
    if request.user.is_authenticated():
        user_profile = get_object_or_404(UserProfile, user=request.user)
        favorite_homes = user_profile.favorites.all()
        return {
            'user_favorite_houses': favorite_homes
        }
    else:
        return {
            'user_favorite_houses': None
        }


def add_visit_home_list_processor(request):
    """
    This context processor adds all the homes that the user indicated they wanted to visit.
    This adds the visit_home_list to the context of the template this processor is added to.
    :param request: The current http request
    :return: Adds the context for all the homes in the visit list
    """
    if request.user.is_authenticated():
        user_profile = get_object_or_404(UserProfile, user=request.user)
        visit_home_list = user_profile.visit_list.all()
        return {
            'user_visit_house_list': visit_home_list
        }
    else:
        return {
            'user_visit_house_list': None
        }


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


