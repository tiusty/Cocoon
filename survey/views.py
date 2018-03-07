# Import Python Modules
import json

# Import Django modules
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

# Import Global config variables
from Cocoon.settings.Global_Config import survey_types, DEFAULT_RENT_SURVEY_NAME

# Import House Database modules
from houseDatabase.models import RentDatabaseModel

# Import User Auth modules
from userAuth.models import UserProfile

# Import Survey algorithm modules
from survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from survey.models import RentingSurveyModel
from survey.forms import RentSurveyForm, DestinationForm, RentSurveyFormMini


@login_required
def renting_survey(request):
    # Create the two forms,
    # RentSurveyForm contains everything except for destinations
    form = RentSurveyForm()

    # DestinationFrom contains the destination
    # The reason why this is split is because the destination form can be made into a form factory
    # So that multiple destinations can be entered, it is kinda working but I removed the ability to do
    # Multiple DestinationsModel on the frontend
    form_destination = DestinationForm()

    # Retrieve the current profile or return a 404
    current_profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'error_message': [],
    }

    if request.method == 'POST':

        # first validating Destination form
        form_destination = DestinationForm(request.POST)
        # create a form instance and populate it with data from the request:
        form = RentSurveyForm(request.POST)

        # Check to see if the designations are valid
        if form_destination.is_valid():
            # check whether it is valid
            if form.is_valid():
                # process the data in form.cleaned_data as required
                rent_survey = form.save(commit=False)
                # Need to retrieve the current userProfile to link the survey to

                # Add the current user to the survey
                rent_survey.user_profile = current_profile

                # Given the enumeration, set the survey to either rent or buy
                # This can probably be removed after testing it
                rent_survey.survey_type = survey_types.rent.value

                # Try seeing if there is already a recent survey and if there is
                # Then delete it. We only want to keep one "recent" survey
                # The user has the option to change the name of it to save it permanently
                RentingSurveyModel.objects.filter(user_profile_survey=current_profile).filter(
                    name_survey=DEFAULT_RENT_SURVEY_NAME).delete()
                rent_survey.save()

                # Since commit=False in the save, need to save the many to many fields
                # After saving the form
                form.save_m2m()

                # Save the destination forms
                destinations = form_destination.save(commit=False)
                # Set the foreign field from the destination to the corresponding survey
                destinations.survey = rent_survey
                destinations.save()

                # redirect to survey result on success:
                return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                    kwargs={"survey_id": rent_survey.id}))
            else:
                context['error_message'].append("The survey form is not valid")
        else:
            # If the destination form is not valid, also do a quick test of the survey field to
            # Inform the user if the survey is also invalid
            if not form.is_valid():
                context['error_message'].append("The normal form is also not valid")
            context['error_message'].append("Destination form is not valid")
    return render(request, 'survey/rentingSurvey.html', {'form': form, 'form_destination': form_destination})


def run_rent_algorithm(survey, context):
    """
    Runs the rent algorithm when the survey is being processed.
    :param survey: (RentingSurveyModel): The survey that the user filled out
    :param context: (dictionary): The context for the template
    """

    # Initialize the rent_algorithm class with empty data
    rent_algorithm = RentAlgorithm()

    """
    STEP 1: Populate the rent_algorithm with all the information from the survey
    """
    rent_algorithm.populate_with_survey_information(survey)

    """
    STEP 2: Compute the approximate distance using zip codes from the possible homes and the desired destinations.
    This also will store how long the commute will take which will be used later for Dynamic filtering/scoring
    """
    rent_algorithm.retrieve_all_approximate_commutes()

    """
    STEP 3: Remove homes that are too far away using approximate commutes
    """
    rent_algorithm.run_compute_approximate_commute_filter()

    """
    STEP 4: Generate scores based on hybrid questions
    """
    rent_algorithm.run_compute_commute_score_approximate()
    rent_algorithm.run_compute_price_score()
    rent_algorithm.run_compute_weighted_score_interior_amenities(survey.air_conditioning,
                                                                 survey.interior_washer_dryer,
                                                                 survey.dish_washer,
                                                                 survey.bath)
    """
    STEP 5: Now sort all the homes from best homes to worst home
    """
    rent_algorithm.run_sort_home_by_score()

    """
    STEP 6: Compute the exact commute time/distance for best homes
    """
    rent_algorithm.retrieve_exact_commutes()

    """
    STEP 7: Score the top homes based on the exact commute time/distance
    """
    rent_algorithm.run_compute_commute_score_exact()

    """
    STEP 8: Reorder homes again now with the full data
    """
    # Now reorder all the homes with the new information
    rent_algorithm.run_sort_home_by_score()

    # Set template variables
    context['locations'] = rent_algorithm.destinations
    context['houseList'] = rent_algorithm.homes[:200]
    context['commuteType'] = rent_algorithm.commute_type_query.commute_type


# Assumes the survey_id will be passed by the URL if not, then it grabs the most recent survey.
# If it can't find the most recent survey it redirects back to the survey
@login_required
def survey_result_rent(request, survey_id="recent"):
    """
    Survey result rent is the heart of the website where the survey is grabbed and the housing list is created
    Based on the results of the survey. This is specifically for the rent survey
    :param request: (Http Request): The HTTP request object
    :param survey_id: (string): This is the survey id that corresponds to the survey that is desired
        If no id is specified then the latest survey is used
    :return: HttpResponse if everything goes well. It returns a lot of context variables like the housingList
        etc. If something goes wrong then it may redirect back to the survey homePage

    ToDo:
    1. Set a limit on the number of homes that are used for commute times. I would say 50 max, then
        only return the top 20-30 homes to the user
    """
    context = {
        'error_message': [],
    }

    user_profile = get_object_or_404(UserProfile, user=request.user)
    # If no id is specified in the URL, then it attempts to load the recent survey
    # The recent survey is the last survey to be created
    if survey_id == "recent":
        # Try to retrieve the most recent survey, but if there are no surveys, then
        # Redirect back to the homepage
        try:
            survey = RentingSurveyModel.objects.filter(user_profile_survey=user_profile).order_by('-created').first()
        except RentingSurveyModel.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Could not find Survey')
            return HttpResponseRedirect(reverse('homePage:index'))
    else:
        # If the user did not choose recent, then try to grab the survey by it's id
        # If it can't find it or it is not associated with the user, just grab the
        # Recent Survey. If that fails, then redirect back to the home page.
        try:
            survey = RentingSurveyModel.objects.filter(user_profile_survey=user_profile).get(id=survey_id)
        # If the survey ID, does not exist/is not for that user, then return the most recent survey
        except RentingSurveyModel.DoesNotExist:
            context['error_message'].append("Could not find survey id, getting recent survey")
            try:
                survey = RentingSurveyModel.objects.filter(user_profile_survey=user_profile)\
                    .order_by('-created').first()
            except RentingSurveyModel.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Could not find Survey')
                return HttpResponseRedirect(reverse('homePage:index'))

    # Populate form with stored data
    form = RentSurveyFormMini(instance=survey)

    # If a POST message occurs (They submit the mini form) then process it
    # If it fails then keep loading survey result and pass the error messages
    if request.method == 'POST':
        # If a POST occurs, update the form. In the case of an error, then the survey
        # Should be populated by the POST data.
        form = RentSurveyFormMini(request.POST, instance=survey)
        # If the survey is valid then redirect back to the page to reload the changes
        # This will also update the house list
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                kwargs={"survey_id": survey.id}))
        else:
            context['error_message'].append("There are form errors")
            try:
                survey = RentingSurveyModel.objects.get(id=survey.id)
                # Think of better solution for problem
            except RentingSurveyModel.DoesNotExist:
                print("Something really went wrong")
                messages.add_message(request, messages.ERROR, 'Could not find Survey')
                return HttpResponseRedirect(reverse('survey:rentSurveyResult'))

    # Now start executing the Algorithm
    run_rent_algorithm(survey, context)
    context['survey'] = survey
    context['form'] = form
    return render(request, 'survey/surveyResultRent.html', context)


@login_required
def visit_list(request):
    context = {
        'error_message': []
    }

    return render(request, 'survey/visitList.html', context)


#######################################################
# Ajax Requests below
#############################################################

# This is used for ajax request to set house favorites
@login_required
def set_favorite(request):
    """
    Ajax request that sets a home as a favorite. This function just toggles the homes.
    Therefore, if the home is requested, if it already existed in the database as a favorite
    Then it removes it from the favorites. If it was not in the database as a favorite then it favorites it. The return
    value is the current state of the house after toggling the home. It returns a 0 if the home is
    not in the home and returns a 1 if the home is a favorite
    :param request: The HTTP request
    :return: An HTTP response which returns a JSON
        0- house not in favorites
        1- house in favorites
        else:
            - the error message
    """
    if request.method == 'POST':
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            house_id = request.POST.get('fav')
            # Retrieve the house associated with that id
            try:
                house = RentDatabaseModel.objects.get(id=house_id)
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    # If the house is already in the database then remove it and return 0
                    # Which means that it is no longer in the favorites
                    if user_profile.favorites.filter(id=house_id).exists():
                        user_profile.favorites.remove(house)
                        return HttpResponse(json.dumps({"result": "0"}),
                                            content_type="application/json",
                                            )
                    # If the  house is not in the Many to Many then add it and
                    # return 1 which means it is currently in the favorites
                    else:
                        user_profile.favorites.add(house)
                        return HttpResponse(json.dumps({"result": "1"}),
                                            content_type="application/json",
                                            )
                except UserProfile.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                        content_type="application/json",
                                        )
            # Return an error is the house cannot be found
            except RentDatabaseModel.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve house"}),
                                    content_type="application/json",
                                    )


@login_required
def delete_survey(request):
    """
    Deletes the given Survey passed by the User.
    It only deletes the survey if the survey corresponds to the given user.
    Always returns to the profile page of the renting survey
    :param request: HTTP request object
    :return:
        0 if the survey was successfully deleted
        error message if the survey was not successfully deleted
    """
    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            survey_id = request.POST.get('survey')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    survey_delete = user_profile.rentingsurveymodel_set.get(id=survey_id)
                    survey_delete.delete()
                    return HttpResponse(json.dumps({"result": "0"}),
                                        content_type="application/json",
                                        )

                except RentingSurveyModel.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Survey"}),
                                        content_type="application/json",
                                        )
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
def set_visit_house(request):
    """
    This ajax function adds a house to the users visit list
    :param request: Http request
    :return: 1 means the home has successfully added
    """

    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            home_id = request.POST.get('visit_id')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    home = RentDatabaseModel.objects.get(id=home_id)
                    user_profile.visit_list.add(home)
                    return HttpResponse(json.dumps({"result": "1",
                                                    "homeId": home_id}),
                                        content_type="application/json", )
                except RentDatabaseModel.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Home"}),
                                        content_type="application/json",
                                        )
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
def delete_visit_house(request):
    """
    This ajax function removes a house from the users visit list
    :param request: Http request
    :return: 0 means the home was successfully removed
    """

    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            home_id = request.POST.get('visit_id')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    home = RentDatabaseModel.objects.get(id=home_id)
                    user_profile.visit_list.remove(home)
                    return HttpResponse(json.dumps({"result": "0"}),
                                        content_type="application/json", )
                except RentDatabaseModel.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Home"}),
                                        content_type="application/json",
                                        )
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
