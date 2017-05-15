import json
import math

import googlemaps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from Unicorn.settings.Global_Config import survey_types, Hybrid_weighted_max, weight_question_value
from houseDatabase.models import RentDatabase
from survey.models import RentingSurveyModel, default_rent_survey_name
from userAuth.models import UserProfile
from .forms import RentSurvey, BuySurvey, DestinationForm, RentSurveyMini


# Create your views here.
@login_required
def renting_survey(request):
    # Create the two forms,
    # RentSurvey contains everything except for destinations
    form = RentSurvey()

    # DestinationFrom contains the destination
    # The reason why this is split is because the destination form can be made into a form factory
    # So that multiple destinations can be entered, it is kinda working but I removed the ability to do
    # Multiple Destinations on the frontend
    formDest = DestinationForm()

    context = {
        'error_message': [],
    }
    if request.method == 'POST':

        # first validating Destination form
        formDest = DestinationForm(request.POST)
        # create a form instance and populate it with data from the request:
        form = RentSurvey(request.POST)

        # Check to see if the designations are valid
        if formDest.is_valid():
            # check whether it is valid
            if form.is_valid():
                # process the data in form.cleaned_data as required
                rentingSurvey = form.save(commit=False)
                currProf = UserProfile.objects.get(user=request.user)
                # Need to retrieve the current userProfile to link the survey to
                try:
                    # Add the current user to the survey
                    rentingSurvey.userProf = currProf
                    # Given the enumeration, set the survey to either rent or buy
                    # This can probably be removed after testing it
                    rentingSurvey.survey_type = survey_types.rent.value

                    # Try seeing if there is already a recent survey and if there is
                    # Then delete it. We only want to keep one "recent" survey
                    # The user has the option to change the name of it to save it permanently
                    try:
                        RentingSurveyModel.objects.filter(userProf=currProf).filter(
                            name=default_rent_survey_name).delete()
                    except RentingSurveyModel.DoesNotExist:
                        print("No surveys to delete")
                    rentingSurvey.save()
                    # Since commit =False in the save, need to save the many to many fields
                    # After saving the form
                    form.save_m2m()

                    # After saving the destination form, retrieve the survey again
                    try:
                        survey = RentingSurveyModel.objects.filter(userProf=currProf).get(id=rentingSurvey.id)
                        destinations = formDest.save(commit=False)
                        # Set the foreign field from the destination to the corresponding survey
                        destinations.survey = survey
                        destinations.save()
                    except RentingSurveyModel.DoesNotExist:
                        raise "Could not retrieve object to attach destinations"
                    # redirect to new URL:
                    print(rentingSurvey.id)
                    return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                        kwargs={"survey_id": rentingSurvey.id}))
                except UserProfile.DoesNotExist:
                    context['error_message'].append("Could not retrieve the User Profile")
            else:
                context['error_message'].append("The survey form is not valid")
        else:
            # If the destination form is not valid, also do a quick test of the survey field to
            # Inform the user if the survey is also invalid
            if not form.is_valid():
                context['error_message'].append("The normal form is also not valid")
            context['error_message'].append("Destination form is not valid")
    return render(request, 'survey/rentingSurvey.html', {'form': form, 'formDest': formDest})


# Function is not implemented, it will basically be the same as the rent survey but for buying instead
@login_required
def buying_survey(request):
    form = BuySurvey()
    return render(request, 'survey/buyingSurvey.html', {'form': form})


class ScoringStruct:
    """
    Class that stores one home and the corresponding information for that home
    This is used to rank homes and eliminate them if necessary
    This also makes sure that the scores are easily associated with the home
    Contains functions to easily extract information for the given home
    """

    def __init__(self, new_house):
        self.house = new_house
        self.score = 0
        self.scorePossible = 0
        self.commuteTime = []
        self.eliminated = False

    def get_score(self):
        """
        Generates the actual score based on the possible score and current score.
        This makes sure that the divide by zero case is handled.
        :return:
            Returns the score. If it was eliminated then it returns -1 to indicate that
                The house should not be used
        """
        # Takes care of divide by 0, also if it is eliminated the score should be -1
        if self.scorePossible != 0 and self.eliminated is False:
            return (self.score / self.scorePossible) * 100
        elif self.eliminated:
            # If eliminated return negative one so it is sorted to the back
            return -1
        else:
            return 0

    def get_user_score(self):
        """
        Function: get_user_score()
        Description:
        Returns a human readable score. Therefore, the user will not see
            a long float which is meaningless
        Comments:
        Currently the scale is to large. Will define to +/- later.
        """
        current_score = self.get_score()
        if current_score >= 90:
            return "A"
        elif current_score >= 80:
            return "B"
        elif current_score >= 70:
            return "C"
        elif current_score >= 60:
            return "D"
        else:
            return "F"

    def get_commute_times(self):
        """
        Returns a formatted string that returns all the commute times for a given home
        Example output:
        27 Minutes, 27 Minutes, 27 Minutes
        :return:
        string -> Formatted to display nicely to the user
        """
        end_result = ""
        counter = 0
        for commute in self.commuteTime:
            if commute > 60:
                max_output = str(int(math.floor(commute / 60))) + " hours " + str(int(commute % 60)) + " Minutes"
            else:
                max_output = str(int(commute)) + " Minutes"
            if counter != 0:
                end_result = end_result + ", " + max_output
            else:
                end_result = max_output
            counter = 1

        return end_result


# It will take in the houseMatrix score
# It will commute the score based on the commute times to the destinations
# The score is multiplied by the scale factor which is user determined
# This factor determines how much the factor will affect the overall weight
def create_commute_score(scored_house_list, survey):
    """
    Evaluates a score based on the commute times.
    Currently if any commute is below the minimum commute time chosen by the user then it is eliminated.
    Also, if the commute time is above the desired commute time, then it is also eliminated.
    If it is in the middle, then anything below 10 minutes is always perfect, then the rest of the times
    are scaled appropriately.

    The User can define a commute weight. If the commute weight is 0, then the scaling factor is 0 so all
    homes are weighted the same as long as they are within the range. As the scaling factor increases, it
    gives a large weight to homes that are closer.
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The Survey is passed, but is only really needed to find the max and min commute times
    :return:
        Returns the ScoringStruct but with the housing scores updated with the commute times and
            appropriate homes eliminated
    """
    # Currently only scores based on commute times
    # It supports having multiple destinations
    max_commute = survey.maxCommute
    min_commute = survey.minCommute
    scale_factor = survey.commuteWeight
    for house in scored_house_list:
        # It needs to be made clear that the scale factor only effects the homes that are under the
        # Commute time. For example, if the max commute is 12 minutes, then anything over 12 is removed.
        # If the scale factor is 0, then all the homes under 12 are weighted equally at 0. Likewise if
        # the scale factor is 5, then a home with a commute time of 6 minutes will have a much higher score then
        # a commute of 9 minutes even though in reality it isn't that much.
        for commute in house.commuteTime:
            # Minimum range is always 10
            if max_commute > 11:
                range_com = max_commute
            else:
                # Make sure that the minimum is 11, so that when it subtracts 10, it doesn't do
                # a divide by zero
                range_com = 11
            # First check to see if the commute is less then the minimum commute, if it is then remove it
            # Second check if the commute time is less than 10 minutes, because if it is it is a perfect score
            # Third If the commute is less than the max commute time compute a score
            # Forth if the commute is more than the maxCommute then remove the house
            if commute < min_commute:
                # Mark house for deletion
                house.eliminated = True
            elif commute <= 10:
                house.score += (100 * scale_factor)
                house.scorePossible += (100 * scale_factor)
            elif commute <= max_commute:
                house.score += (((1 - (commute - 10) / (range_com - 10)) * 100) * scale_factor)
                house.scorePossible += (100 * scale_factor)
            else:
                # Mark house for deletion
                house.eliminated = True
    return scored_house_list


def create_price_score(scored_house_list, survey):
    """
    Generates the score according to the price of the home
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The survey that the homes are being filtered by
    :return:
    """

    # Retrieve all the constant values
    max_price = survey.maxPrice
    min_price = survey.minPrice
    scale_factor = survey.price_weight

    # Apply price scoring for all the houses
    for house in scored_house_list:
        house_price = house.house.get_price()
        house_price_normalized = house_price - min_price
        # Guarantee that the house normalized price is not negative, (score should never decrease)
        if house_price_normalized >= 0:
            house_range = max_price - min_price
            # Make sure that the house range is never negative (score should never decrease)
            if house_range > 0:
                house.score += ((1 - house_price_normalized / house_range) * 100) * scale_factor
                house.scorePossible += (100 * scale_factor)
            # This takes care of the divide by zero case
            # If the range is zero, then the max and min price should be the same
            # Therefore assuming that the static filter worked before, the house price
            # Needs to be between the max and minimum price and therefore, in this case,
            # The house price should be equal to the min price. Therefore, if this case occurs
            # Do an extra validation to make sure that the min_price equals the house price to
            # Prevent an error
            elif house_range == 0 and house_price == min_price:
                house.score += 100 * scale_factor
                house.scorePossible += 100 * scale_factor


def weighted_question_scoring(home, contains_item, scale_factor):
    """
    This is the function that determines the weight of a given weight question
    This allows a constant method of determining the score and thus makes it
    Easier to change later
    :param home: This is a home given as a single house structure
    :param contains_item: This is a boolean that says whether or not the given home
        has the item that is being tested for, i.e does it have an airconditioning?
    :param scale_factor: This is an integer which is the weighted value that the user
        gave the question. Therefore, the higher the scale factor, the more the question
        affects the weight
    """

    # First condition is if the user gave the max weight to the factor then it is a
    # must have. Therefore, if the home doesn't have it then eliminate the home
    if scale_factor == Hybrid_weighted_max - 1 and contains_item is False:
        home.eliminated = True
    # If the home contains the item then add points torwads this home. This means
    # The home got a 100% so the score will go up.
    elif contains_item:
        home.score += scale_factor * weight_question_value
    # Regardless of anything else, always increment the possible points depending on the
    # Scale factor. If the home had the item then the home will benifit more, if the home
    # didn't have the item, then the higher the scale factor the more negatively it will be
    # Affected
    home.scorePossible += scale_factor * weight_question_value


def create_interior_amenities_score(scored_house_list, survey):
    """
    Updates the houes scoresd based on the interior amenities questions
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The user survey that is being used to evaluate the homes
    """
    # Loop throuh all the homes and score each one
    for home in scored_house_list:
        weighted_question_scoring(home, home.house.has_air_conditioning(), survey.airConditioning)
        weighted_question_scoring(home, home.house.has_wash_dryer_in_home(), survey.washDryer_InHome)
        weighted_question_scoring(home, home.house.has_dish_washer(), survey.dishWasher)
        weighted_question_scoring(home, home.house.has_bath(), survey.bath)


# Given the houseScore and the survey generate and add the score based
# On the commute times to the destinations
def create_house_score(house_list_scored, survey):
    """
    All the functions that perform scoring will be listed here
    :param house_list_scored: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param survey: The current survey, since the scoring is based on the result of the survey
    :return: The house structure with the homes scored
    """
    # Creates score based on commute
    create_commute_score(house_list_scored, survey)
    create_price_score(house_list_scored, survey)
    create_interior_amenities_score(house_list_scored, survey)
    return house_list_scored


# Function takes in the ScoringStruct and returns the sorted list
def order_by_house_score(scored_house_list):
    """
    Orders the homes based on the current score
    The high scored home will be put at the front of the list
    Homes that are eliminated have no order
    :param scored_house_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :return: The house structure but sorted based on the home score
    """
    # Simple insertion sort to sort houses by score
    for index in range(1, len(scored_house_list)):
        current_value = scored_house_list[index]
        position = index

        while position > 0 and scored_house_list[position - 1].get_score() < current_value.get_score():
            scored_house_list[position] = scored_house_list[position - 1]
            position -= 1

        scored_house_list[position] = current_value

    return scored_house_list


def google_matrix(origins, destinations, scored_list, context):
    """
    Generates the Commute times for all the homes
    :param origins: All the origin locations, in this case, all the filter_homes
    :param destinations: All the destinations, what the user puts in as destinations
    :param scored_list: The array of ScoringStructs which holds all the homes that
        have already gone past static filtering
    :param context: Context that will be passed to the template
    :return: Returns the scored list with all the commute times entered
    """

    # Generates matrix of commute times from the origin to the destination
    gmaps = googlemaps.Client(key='AIzaSyBuecmo6t0vxQDhC7dn_XbYqOu0ieNmO74')

    # Can add things to the arguments, like traffic_model, avoid things, depature_time etc
    # Each row contains the origin with each corresponding destination
    # The value field of duration is in seconds
    mode_commute = "driving"
    measure_units = "imperial"
    matrix = gmaps.distance_matrix(origins, destinations,
                                   mode=mode_commute,
                                   units=measure_units,
                                   )
    # Only if the matrix is defined should the calculations occur, otherwise throw an error
    if matrix:
        # Try to think of a better way than a simple counter
        counter = 0
        for house in scored_list:
            for commute in matrix["rows"][counter]["elements"]:
                # Divide by 60 to get minutes
                if commute['status'] == 'OK':
                    house.commuteTime.append(commute['duration']["value"] / 60)
                else:
                    # Eliminate houses that can't have a commute value
                    house.eliminated = True
            counter += 1
            # Only Add the context if the commute is able to be processed
        context['commuteMode'] = mode_commute
    else:
        context['error_message'].append("Couldn't calculate distances, something went wrong")

    return scored_list


def start_algorithm(survey, user_profile, context):
    # Creates an array with all the home types indicated by the survey
    home_types = []
    for home in survey.home_type.all():
        home_types.append(home.homeType)

    # Filters the Database with all the static elements as the first pass
    """
    The item that will filter the list the most should be first to narrow down the number of iterations
    The database needs to be searched
    (Right now it isn't order by efficiency but instead by when it was added. Later it can be switched around

    Current order:
    1. Filter by price range. The House must be in the correct range to be accepted
    2. Filter by Home Type. The home must be the correct home type to be accepted
    3. Filter by Move In day. The two move in days create the range that is allowed. The range is inclusive
        If the house is outside the range it is eliminated
    4. Filter by the number of bed rooms. It must be the correct number of bed rooms to work.
    4. Filter by the number of bathrooms
    """
    filtered_house_list = RentDatabase.objects \
        .filter(price__range=(survey.minPrice, survey.maxPrice)) \
        .filter(home_type__in=home_types) \
        .filter(moveInDay__range=(survey.moveinDateStart, survey.moveinDateEnd)) \
        .filter(numBedrooms=survey.numBedrooms) \
        .filter(numBathrooms__range=(survey.minBathrooms, survey.maxBathrooms))

    # Retrieves all the destinations that the user recorded
    destination_set = survey.rentingdesintations_set.all()

    # First put all the origins into an array then the destinations
    origins = []
    for house in filtered_house_list:
        origins.append(house.address)

    destinations = []
    for location in destination_set:
        destinations.append(location.full_address())

    # This puts all the homes into a scored list
    scored_house_list = []
    for house in filtered_house_list:
        scored_house_list.append(ScoringStruct(house))

    # First Commute score is calculated if there are origins and destinations
    if not destinations or not origins:
        context['error_message'].append("No Destination or origin")
    else:
        scored_house_list = google_matrix(origins, destinations, scored_house_list, context)

    # Generate scores for the homes based on the survey results
    homes_fully_scored = create_house_score(scored_house_list, survey)

    # Order the homes based off the score
    scored_house_list_ordered = order_by_house_score(homes_fully_scored)

    # Contains destinations of the user
    context['locations'] = destination_set
    # House list either comes from the scored homes or from the database static list if something went wrong
    # Only put up to 35 house on the list
    context['houseList'] = scored_house_list_ordered[:35]


# Assumes the survey_id will be passed by the URL if not, then it grabs the most recent survey.
# If it can't find the most recent survey it redirects back to the survey
@login_required
def survey_result_rent(request, survey_id="recent"):
    """
    Survey result rent is the heart of the website where the survey is grabbed and the housing list is created
    Based on the results of the survey. This is specifically for the rent survey
    :param request: Http Request
    :param survey_id:  This is the survey id that corresponds to the survey that is desired
        If no id is specified then the latest survey is used
    :return: HttpResponse if everything goes well. It returns a lot of context variables like the housingList
        etc. If something goes wrong then it may redirect back to the survey homePage

    To Do:
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
            survey = RentingSurveyModel.objects.filter(userProf=user_profile).order_by('-created').first()
        except RentingSurveyModel.DoesNotExist:
            return HttpResponseRedirect(reverse('homePage:index'))
    else:
        # If the user did not choose recent, then try to grab the survey by it's id
        # If it can't find it or it is not associated with the user, just grab the
        # Recent Survey. If that fails, then redirect back to the home page.
        try:
            survey = RentingSurveyModel.objects.filter(userProf=user_profile).get(id=survey_id)
        # If the survey ID, does not exist/is not for that user, then return the most recent survey
        except RentingSurveyModel.DoesNotExist:
            context['error_message'].append("Could not find survey id, getting recent survey")
            try:
                survey = RentingSurveyModel.objects.filter(userProf=user_profile).order_by('-created').first()
            except RentingSurveyModel.DoesNotExist:
                return HttpResponseRedirect(reverse('homePage:index'))
    # Populate form with stored data
    form = RentSurveyMini(instance=survey)

    # If a POST message occurs (They submit the mini form) then process it
    # If it fails then keep loading survey result and pass the error messages
    if request.method == 'POST':
        # If a POST occurs, update the form. In the case of an error, then the survey
        # Should be populated by the POST data.
        form = RentSurveyMini(request.POST, instance=survey)
        # If the survey is valid then redirect back to the page to reload the changes
        # This will also update the house list
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                                kwargs={"survey_id": survey.id}))
        else:
            context['error_message'].append("There are form errors")

    # Now start executing the Algorithm
    start_algorithm(survey, user_profile, context)
    context['survey'] = survey
    context['form'] = form

    return render(request, 'survey/surveyResultRent.html', context)


@login_required
def visit_list(request):

    context = {
        'error_message': []
    }
    user_profile = get_object_or_404(UserProfile, user=request.user)
    visit_list_set = user_profile.visit_list.all()

    context['visit_list_set'] = visit_list_set
    print(context)
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
    Then it unfavorites it. If it was not in the database as a favorite then it favorites it. The return
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
                house = RentDatabase.objects.get(id=house_id)
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
            except RentDatabase.DoesNotExist:
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
                    home = RentDatabase.objects.get(id=home_id)
                    user_profile.visit_list.add(home)
                    return HttpResponse(json.dumps({"result": "1"}),
                                        content_type="application/json",)
                except RentDatabase.DoesNotExist:
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
                    home = RentDatabase.objects.get(id=home_id)
                    user_profile.visit_list.remove(home)
                    return HttpResponse(json.dumps({"result": "0"}),
                                        content_type="application/json", )
                except RentDatabase.DoesNotExist:
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