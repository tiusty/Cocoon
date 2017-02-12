from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RentSurvey, BuySurvey, DestinationForm, RentSurveyMini
from userAuth.models import UserProfile
from survey.models import survey_types, RentingSurveyModel, default_rent_survey_name
from houseDatabase.models import RentDatabase
from django.contrib.auth.decorators import login_required
import math

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
                    rentingSurvey.userProf = currProf
                    rentingSurvey.survey_type = survey_types.rent.value
                    # Try seeing if there is already a recent survey and if there is
                    # Then delete it. We only want to keep one "recent" survey
                    # The user has the option to change the name of it to save it permanently
                    try:
                        surveyName = default_rent_survey_name
                        currRecentSur = RentingSurveyModel.objects.filter(userProf=currProf).filter(name=surveyName).delete()
                    except RentingSurveyModel.DoesNotExist:
                        print("No surveys to delete")
                    rentingSurvey.save()
                    # Since commit =False in the save, need to save the many to many fields
                    # After saving the form
                    form.save_m2m()

                    # After saving the destination form, retrieve the survey again
                    try:
                        survey = RentingSurveyModel.objects.filter(userProf=currProf).get(name=surveyName)
                        destinations = formDest.save(commit=False)
                        # Set the foreign field from the destination to the corresponding survey
                        destinations.survey = survey
                        destinations.save()
                    except RentingSurveyModel.DoesNotExist:
                        raise "Could not retrieve object to attach destinations"
                    # redirect to new URL:
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
def buying_survey(request):
    form = BuySurvey()
    return render(request, 'survey/buyingSurvey.html', {'form':form})


# This struct allows each home to easily be associated with a score and appropriate data
@login_required
class ScoringStruct:
    def __init__(self, newHouse):
        self.house = newHouse
        self.score = 0
        self.scorePossible = 0
        self.commuteTime = []
        self.eliminated = False

    # Generates the actual "score" for the house
    def get_score(self):
        # Takes care of divide by 0, also if it is eleminted the score should be zero
        if self.scorePossible != 0 and self.eliminated is False:
            return (self.score/self.scorePossible)*100
        else:
            return 0

    def get_commute_times(self):
        endResult=""
        counter = 0;
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
def create_house_score(houseScore, survey):
    # Currently only scores based on commute times
    # It supports having multiple destinations
    maxCommute = survey.maxCommute
    for house in houseScore:
        for commute in house.commuteTime:
            # Minimum range is always 10
            if maxCommute > 11:
                rangeCom = maxCommute
            else:
                rangeCom = 11
            # IF the commute is less than 10 minutes make it perfect
            if commute <= 10:
                house.score += 100
                house.scorePossible += 100
            elif commute <= maxCommute:
                house.score += (1 - (commute-10)/(rangeCom - 10))*100
                house.scorePossible += 100
            else:
                # Mark house for deletion
                house.eliminated = True
    return houseScore


# Function takes in the ScoringStruct and returns the sorted list
def order_by_house_score(houseScore):
    # Simple insertion sort to sort houses by score
    for index in range(1, len(houseScore)):
        currentValue = houseScore[index]
        position = index

        while position > 0 and houseScore[position-1].get_score()<currentValue.get_score():
            houseScore[position]=houseScore[position-1]
            position=position-1

        houseScore[position]=currentValue

    # Puts homes into an array ordered by score so it is easier to parse in template
    # Also, it is the same(simliar) format has the default housing list if the matrix can't get generated
    #sortedHomes = []
    #for house in houseScore:
    #    sortedHomes.append(house.house)

    #return sortedHomes
    return houseScore


# Assumes the survey_id will be passed by the URL if not, then it grabs the most recent survey.
# If it can't find the most recent survey it redirects back to the survey
@login_required
def survey_result(request, survey_type, survey_id="recent"):
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
                housingList = RentDatabase.objects.filter(price__range=(survey.minPrice, survey.maxPrice))\
                    .filter(home_type__in=homeTypes)

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
                            for commute in matrix["rows"][counter]["elements"]:
                                print(commute)
                                # Divide by 60 to get minutes
                                if(commute['status'] == 'OK'):
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
