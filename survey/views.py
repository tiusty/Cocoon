from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import RentSurvey, BuySurvey, DestinationForm, RentSurveyMini
from userAuth.models import UserProfile
from survey.models import survey_types, RentingSurveyModel, default_rent_survey_name
from houseDatabase.models import RentDatabase
from django.contrib.auth.decorators import login_required
import math
import json

import googlemaps


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
                        RentingSurveyModel.objects.filter(userProf=currProf).filter(name=default_rent_survey_name).delete()
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
                    return HttpResponseRedirect(reverse('survey:surveyResult',
                                                        kwargs={'survey_type':"rent", "survey_id": rentingSurvey.id}))
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
    return render(request, 'survey/rentingSurvey.html', {'form': form, 'formDest':formDest})


# Function is not implemented, it will basically be the same as the rent survey but for buying instead
@login_required
def buying_survey(request):
    form = BuySurvey()
    return render(request, 'survey/buyingSurvey.html', {'form':form})


class ScoringStruct:
    """
    Class that stores one home and the corresponding information for that home
    This is used to rank homes and eliminate them if necessary
    This also makes sure that the scores are easily associated with the home
    Contains functions to easily extract information for the given home
    """
    def __init__(self, newHouse):
        self.house = newHouse
        self.score = 0
        self.scorePossible = 0
        self.commuteTime = []
        self.eliminated = False
        self.favorite = False

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
            return (self.score/self.scorePossible)*100
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
        currScore = self.get_score()
        if currScore >= 90:
            return "A"
        elif currScore >= 80:
            return "B"
        elif currScore >= 70:
            return "C"
        elif currScore >= 60:
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
        endResult=""
        counter = 0
        for commute in self.commuteTime:
            if commute > 60:
                maxOutput = str(int(math.floor(commute / 60))) + " hours " + str(int(commute % 60)) + " Minutes"
            else:
                maxOutput = str(int(commute)) + " Minutes"
            if counter != 0:
                endResult = endResult+", "+maxOutput
            else:
                endResult = maxOutput
            counter = 1

        return endResult


# It will take in the houseMatrix score
# It will commute the score based on the commute times to the destinations
# The score is multiplied by the scale factor which is user determined
# This factor determines how much the factor will affect the overall weight
def create_commute_score(houseScore, survey):
    """
    Evaluates a score based on the commute times.
    Currently if any commute is below the minimum commute time chosen by the user then it is eliminated.
    Also, if the commute time is above the desired commute time, then it is also eliminated.
    If it is in the middle, then anything below 10 minutes is always perfect, then the rest of the times
    are scaled appropriately.

    The User can define a commute weight. If the commute weight is 0, then the scaling factor is 0 so all
    homes are weighted the same as long as they are within the range. As the scaling factor increases, it
    gives a large weight to homes that are closer.
    :param houseScore: ScoringStruct that stores all the homes and the corresponding commute times
    :param survey: The Survey is passed, but is only really needed to find the max and min commute times
    :return:
        Returns the ScoringStruct but with the housing scores updated with the commute times and
            appropriate homes eliminated
    """
    # Currently only scores based on commute times
    # It supports having multiple destinations
    maxCommute = survey.maxCommute
    minCommute = survey.minCommute
    scaleFactor = survey.commuteWeight
    for house in houseScore:
        # It needs to be made clear that the scale factor only effects the homes that are under the
        # Commute time. For example, if the max commute is 12 minutes, then anything over 12 is removed.
        # If the scale factor is 0, then all the homes under 12 are weighted equally at 0. Likewise if
        # the scale factor is 5, then a home with a commute time of 6 minutes will have a much higher score then
        # a commute of 9 minutes even though in reality it isn't that much.
        for commute in house.commuteTime:
            # Minimum range is always 10
            if maxCommute > 11:
                rangeCom = maxCommute
            else:
                # Make sure that the minimum is 11, so that when it subtracts 10, it doesn't do
                # a divide by zero
                rangeCom = 11
            # First check to see if the commute is less then the minimum commute, if it is then remove it
            # Second check if the commute time is less than 10 minutes, because if it is it is a perfect score
            # Third If the commute is less than the max commute time compute a score
            # Forth if the commute is more than the maxCommute then remove the house
            if commute < minCommute:
                # Mark house for deletion
                house.eliminated = True
            elif commute <= 10:
                house.score += (100 * scaleFactor)
                house.scorePossible += (100 * scaleFactor)
            elif commute <= maxCommute:
                house.score += (((1 - (commute-10)/(rangeCom - 10))*100) * scaleFactor)
                house.scorePossible += (100 * scaleFactor)
            else:
                # Mark house for deletion
                house.eliminated = True
    return houseScore


# Given the houseScore and the survey generate and add the score based
# On the commute times to the destinations
def create_house_score(houseScore, survey):

    # Creates score based on commute
    create_commute_score(houseScore, survey)
    return houseScore


# Function takes in the ScoringStruct and returns the sorted list
def order_by_house_score(houseScore):
    # Simple insertion sort to sort houses by score
    for index in range(1, len(houseScore)):
        currentValue = houseScore[index]
        position = index

        while position > 0 and houseScore[position-1].get_score()<currentValue.get_score():
            houseScore[position]=houseScore[position-1]
            position -= 1

        houseScore[position] = currentValue

    return houseScore


# Assumes the survey_id will be passed by the URL if not, then it grabs the most recent survey.
# If it can't find the most recent survey it redirects back to the survey
@login_required
def survey_result(request, survey_type, survey_id="recent"):
    """
    Survey result is the heart of the website where the survey is grabbed and the housing list is created
    Based on the results of the survey.
    :param request: Http Request
    :param survey_type: This is the survey_type which currently is one or rent or buy
    :param survey_id:  This is the survey id that corresponds to the survey that is desired
        If no id is specified then the latest survey is used
    :return: HttpResponse if everything goes well. It returns a lot of context variables like the housingList
        etc. If something goes wrong then it may redirect back to the survey homePage

    To Do:
    1. Set a limit on the number of homes that are used for commute times. I would say 50 max, then
        only return the top 20-30 homes to the user
    2. Set the moveInDay to a period so people can specify a range of dates to check
    """
    context = {
        'error_message': [],
    }

    # If the mini form was posted, then save the results before reloading the page
    if request.method == 'POST':
        try:
            currProf = UserProfile.objects.get(user=request.user)
            try:
                survey = RentingSurveyModel.objects.filter(userProf=currProf).get(id=survey_id)
                form = RentSurveyMini(request.POST, instance=survey)
                # If the form is valid, then save the updates to that survey and redirect back to survey results
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('survey:surveyResult',
                                                        kwargs={'survey_type': "rent", "survey_id": survey.id}))
                else:
                    context['error_message'].append("The survey was POSTed incorrectly")
            except RentingSurveyModel.DoesNotExist:
                context['error_message'].append("Survey does not exist")
        except UserProfile.DoesNotExist:
            context['error_message'].append("User profile doesn't exist")

    # If the survey was not successfully posted or if no POST, then populate the page
    if survey_type == "rent":
        try:
            currProf = UserProfile.objects.get(user=request.user)
            try:
                # If no id is specified in the URL, then it attempts to load the recent survey
                # The recent survey is the last survey to be created
                if survey_id == "recent":
                    survey = RentingSurveyModel.objects.filter(userProf=currProf).order_by('-created').first()
                else:
                    # If it can't find the survey id, then just get the recent survey
                    try:
                        survey = RentingSurveyModel.objects.filter(userProf=currProf).get(id=survey_id)
                    except RentingSurveyModel.DoesNotExist:
                        context['error_message'].append("Could not find survey id, getting recent survey")
                        survey = RentingSurveyModel.objects.filter(userProf=currProf).order_by('-created').first()

                # Creates an array with all the home types indicated by the survey
                homeTypes = []
                for home in survey.home_type.all():
                    homeTypes.append(home.homeType)

                # Filters the Database with all the static elements as the first pass
                """
                The item that will filter the list the most should be first to narrow down the number of iterations
                The database needs to be searched
                (Right now it isn't order by efficiecy but instead by when it was added. Later it can be switched around

                Current order:
                1. Filter by price range. The House must be in the correct range to be accepted
                2. Filter by Home Type. The home must be the correct home type to be accepted
                3. Filter by Move In day. Currently it filters only by day and month. THe day is ignored
                    The house move in day must by in that month for it to work. (Maybe switch to range later)
                4. Filter by the number of bed rooms. It must be the correct number of bed rooms to work.
                """
                housingList = RentDatabase.objects.filter(
                    price__range=(survey.minPrice, survey.maxPrice))\
                    .filter(home_type__in=homeTypes)\
                    .filter(moveInDay__year=survey.moveinDate.year, moveInDay__month=survey.moveinDate.month)\
                    .filter(numBedrooms=survey.numBedrooms)

                # Retrieves all the destinations that the user recorded
                locations = survey.rentingdesintations_set.all()

                # Generates matrix of commute times from the origin to the destination
                gmaps = googlemaps.Client(key='AIzaSyBuecmo6t0vxQDhC7dn_XbYqOu0ieNmO74')

                # First put all the origins into an array then the destinations
                origins = []
                for house in housingList:
                    origins.append(house.address)

                destinations = []
                for location in locations:
                    destinations.append(location.full_address())

                # Need to better define error cases.
                # Also, put more try blocks in case of error
                if not destinations or not origins:
                    print("No destinations or origins")
                    context['error_message'].append("No Destination or origin")
                else:
                    # Can add things to the arguments, like traffic_model, avoid things, depature_time etc
                    # Each row contains the origin with each corresponding destination
                    # The value field of duration is in seconds
                    modeCommute="driving"
                    context['commuteMode'] = modeCommute
                    matrix = gmaps.distance_matrix(origins, destinations,
                                                   mode=modeCommute,
                                                   units="imperial",
                                                   )
                    # Only if the matrix is defined should the calculations occur, otherwise throw an error
                    if matrix:
                        print(matrix)
                        # While iterating through all the destinations, put homes into a scoring structure to easily
                        # Keep track of the score for the associated home
                        houseScore = []
                        # Try to think of a better way than a simple counter
                        counter = 0
                        for house in housingList:
                            currHouse = ScoringStruct(house)
                            if currProf.favorites.filter(id=house.id).exists():
                                currHouse.favorite = True
                            for commute in matrix["rows"][counter]["elements"]:
                                print(commute)
                                # Divide by 60 to get minutes
                                if commute['status'] == 'OK':
                                    currHouse.commuteTime.append(commute['duration']["value"]/60)
                                else:
                                    # Eliminate houses that can't have a commute value
                                    currHouse.eliminated = True
                            houseScore.append(currHouse)
                            counter += 1

                        # Generate scores for the homes based on the survey results
                        homesScored = create_house_score(houseScore, survey)

                        # Order the homes based off the score
                        housingList = order_by_house_score(homesScored)
                    else:
                        context['error_message'].append("Couldn't calculate distances, something went wrong")

                context['survey'] = survey
                # Contains destinations of the user
                context['locations'] = locations
                # House list either comes from the scored homes or from the database static list if something went wrong
                context['houseList'] = housingList

                # fill form with data from database
                form = RentSurveyMini(instance=survey)
            except RentingSurveyModel.DoesNotExist:
                context['error_message'].append("Could not retrieve rent survey")
                print("Error, could not find survey id, redirecting back to survey")
                return HttpResponseRedirect(reverse('survey:rentingSurvey'))
        except UserProfile.DoesNotExist:
            context['error_message'].append("Could not find User Profile")
    # For now just return to survey for the buying survey and unknown
    elif survey_type == "buy":
        return HttpResponseRedirect(reverse('survey:rentingSurvey'))
    else:
        return HttpResponseRedirect(reverse('survey:rentingSurvey'))

    context['form'] = form
    return render(request, 'survey/surveyResultRent.html', context)


# This is used for ajax request to set house favorites
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
            houseId = request.POST.get('fav')
            # Retrieve the house associated with that id
            try:
                house = RentDatabase.objects.get(id=houseId)
                try:
                    currProfile = UserProfile.objects.get(user=request.user)
                    # If the house is already in the database then remove it and return 0
                    # Which means that it is no longer in the favorites
                    if currProfile.favorites.filter(id=houseId).exists():
                        currProfile.favorites.remove(house)
                        return HttpResponse(json.dumps({"result": "0"}),
                                            content_type="application/json",
                                            )
                    # If the  house is not in the Many to Many then add it and
                    # return 1 which means it is currently in the favorites
                    else:
                        currProfile.favorites.add(house)
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
