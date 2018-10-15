# Import Python Modules
import json

# Import Django modules
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.forms import inlineformset_factory

# Import Signatures modules
from cocoon.signature.models import HunterDocManagerModel

# Import House Database modules
from cocoon.houseDatabase.models import RentDatabaseModel

# Import User Auth modules
from cocoon.userAuth.models import UserProfile

# Import Survey algorithm modules
from cocoon.survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from cocoon.survey.models import RentingSurveyModel, RentingDestinationsModel
from cocoon.survey.forms import RentSurveyForm, BrokerRentSurveyForm, BrokerRentSurveyFormMini, \
    RentingDestinationsForm, RentSurveyFormMini


@login_required
def renting_survey(request):
    # Create the two forms,
    # RentSurveyForm contains everything except for destinations

    # DestinationFrom contains the destination
    # The reason why this is split is because the destination form can be made into a form factory
    # So that multiple destinations can be entered, it is kinda working but I removed the ability to do
    # Multiple DestinationsModel on the frontend
    number_of_formsets = 4
    number_of_destinations = 1
    DestinationFormSet = inlineformset_factory(RentingSurveyModel, RentingDestinationsModel, extra=number_of_formsets,
                                               form=RentingDestinationsForm, can_delete=False)
    destination_form_set = DestinationFormSet()

    # Retrieve the current profile or return a 404
    current_profile = get_object_or_404(UserProfile, user=request.user)

    if current_profile.user.is_broker:
        form_type = BrokerRentSurveyForm
    else:
        form_type = RentSurveyForm

    form = form_type()

    context = {'error_message': [], 'number_of_formsets': number_of_formsets}

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = form_type(request.POST)

        # check whether it is valid
        if form.is_valid():
            number_of_destinations = int(request.POST['number_destinations_filled_out'])

            # process the data in form.cleaned_data as required
            rent_survey = form.save(commit=False)
            # Need to retrieve the current userProfile to link the survey to

            # Add the current user to the survey
            rent_survey.user_profile = current_profile

            # Create the form destination set
            request_post = request.POST.copy()
            for x in range (number_of_destinations, number_of_formsets):
                for field in request.POST:
                    if 'rentingdestinationsmodel_set-' + str(x) in field:
                        del request_post[field]

            destination_form_set = DestinationFormSet(request_post, instance=rent_survey)

            if destination_form_set.is_valid():

                # Only if all the forms validate will we save it to the database
                rent_survey.save()
                form.save_m2m()
                destination_form_set.save()

                # redirect to survey result on success:
                return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                    kwargs={"survey_url": rent_survey.url}))

            else:
                context['error_message'] = "The destination set did not validate"
                context['error_message'] = destination_form_set.errors
        else:
            # If the destination form is not valid, also do a quick test of the survey field to
            # Inform the user if the survey is also invalid
            context['error_message'].append('The survey did not validate')

    context['form'] = form
    context['form_destination'] = destination_form_set
    context['number_of_destinations'] = number_of_destinations
    return render(request, 'survey/rentingSurvey.html', context)


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
    rent_algorithm.run_compute_weighted_score_exterior_amenities(survey.parking_spot)
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
    context['commuters'] = rent_algorithm.destinations

    # Only return homes that the score is 0 or above
    context['houseList'] = [x for x in rent_algorithm.homes[:50] if x.percent_score() >= 0]


# Assumes the survey_slug will be passed by the URL if not, then it grabs the most recent survey.
# If it can't find the most recent survey it redirects back to the survey
@login_required
def survey_result_rent(request, survey_url=""):
    """
    Survey result rent is the heart of the website where the survey is grabbed and the housing list is created
    Based on the results of the survey. This is specifically for the rent survey
    :param request: (Http Request): The HTTP request object
    :param survey_url: (string): This is the survey slug to determine which survey to load
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

    if user_profile.user.is_broker:
        form_type = BrokerRentSurveyFormMini
    else:
        form_type = RentSurveyFormMini

    # Tries to grab the survey. If the survey name was not passed in, then it grabs the most recent survey taken.
    try:
        survey = RentingSurveyModel.objects.filter(user_profile=user_profile).get(url=survey_url)
    # If the survey ID, does not exist/is not for that user, then return the most recent survey
    except RentingSurveyModel.DoesNotExist:
        if RentingSurveyModel.objects.filter(user_profile=user_profile).exists():
            survey = RentingSurveyModel.objects.filter(user_profile=user_profile)\
                .order_by('created').first()
            messages.add_message(request, messages.WARNING, 'Could not find Survey, loading most recent survey')
            return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                kwargs={"survey_url": survey.url}))
        else:
            messages.add_message(request, messages.ERROR, 'Could not find Survey')
            return HttpResponseRedirect(reverse('homePage:index'))

    # Populate form with stored data
    form = form_type(instance=survey)
    number_of_forms = survey.rentingdestinationsmodel_set.count()
    DestinationFormSet = inlineformset_factory(RentingSurveyModel, RentingDestinationsModel, extra=0,
                                               form=RentingDestinationsForm, can_delete=False)
    destination_form_set = DestinationFormSet(instance=survey)

    # If a POST message occurs (They submit the mini form) then process it
    # If it fails then keep loading survey result and pass the error messages
    if request.method == 'POST':
        # If a POST occurs, update the form. In the case of an error, then the survey
        # Should be populated by the POST data.
        form = form_type(request.POST, instance=survey, user=request.user)
        destination_form_set = DestinationFormSet(request.POST, instance=survey)
        # If the survey is valid then redirect back to the page to reload the changes
        # This will also update the house list
        if form.is_valid():
            if destination_form_set.is_valid():
                form.save()
                destination_form_set.save()
                return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                    kwargs={"survey_url": survey.url}))
            else:
                context['error_message'].append("There are form errors in destinatino form")
                context['error_message'].append(destination_form_set.errors)
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
    context['form_destination'] = destination_form_set
    context['number_of_formsets'] = number_of_forms
    context['number_of_destinations'] = number_of_forms
    context['mini_form'] = True
    messages.add_message(request, messages.INFO, "We've scoured the market to pick your personalized short list of "
                                                 "the best places, now it's your turn to pick your favorites")
    return render(request, 'survey/surveyResultRent.html', context)


@login_required
def visit_list(request):
    context = {
        'error_message': []
    }

    # Retrieve the models
    user_profile = get_object_or_404(UserProfile, user=request.user)
    manager = get_object_or_404(HunterDocManagerModel, user=user_profile.user)

    # Since the page is loading, update all the signed documents to see if the status has changed
    manager.update_all_is_signed()

    # Create context to update the html based on the status of the documents
    context['pre_tour_signed'] = manager.is_pre_tour_signed()
    context['pre_tour_forms_created'] = manager.pre_tour_forms_created()

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


@login_required
def send_documents(request):
    """
    :param request: The HTTP request
    :return: An HTTP response which returns a JSON
        result:
            0- failures
            1- success
        message:
            - the message associated with the request
    """
    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    doc_manager = user_profile.user.doc_manager
                    if not doc_manager.pre_tour_forms_created():
                        if doc_manager.create_pre_tour_documents():
                            return HttpResponse(json.dumps({"result": "1",
                                                            "message": "Document Created"}),
                                                content_type="application/json", )
                        else:
                            return HttpResponse(json.dumps({"result": "1",
                                                            "message": "Document already exists"}),
                                                content_type="application/json", )
                    else:
                        doc_manager.update_all_is_signed()
                        if doc_manager.is_pre_tour_signed():
                            return HttpResponse(json.dumps({"result": "2",
                                                            "message": "Document signed!"}),
                                                content_type="application/json", )
                        else:
                            return HttpResponse(json.dumps({"result": "1",
                                                            "message": "Document still not signed"}),
                                                content_type="application/json", )

                except HunterDocManagerModel.DoesNotExist:
                    return HttpResponse(json.dumps({
                        "result": "0",
                        "message": "Could not retrieve Home"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "0",
                                                "message": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result" : "0",
                                            "message": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "0",
                                        "message": "Method Not POST"}),
                            content_type="application/json",
                            )
