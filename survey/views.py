from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RentSurvey, BuySurvey, DestinationForm, RentSurveyMini
from userAuth.models import UserProfile
from survey.models import survey_types, RentingSurveyModel, default_rent_survey_name
from houseDatabase.models import RentDatabase

import googlemaps


# Create your views here.
def renting_survey(request):
    #!!!!!!!!!!!!!!!! TO DO !!!!!!!!!!!!!!!!!!!!!
    # can't handle anonymous users, either require log in or handle it some how
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


# Function takes in the JSON housing list from the distance matrix
# It will take in the houseMatrix score
def create_house_score(houseMatrix, houseList, survey):
    print(houseMatrix["rows"][0])
    # For now just printing out all the distance and commute times
    for house in houseMatrix["rows"]:
        print(house)


# This is different because the survey id is passed as a variable
def survey_result(request, survey_type, survey_id="recent"):
    context = {
        'error_message': [],
    }

    form = RentSurveyMini()
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
                # Recent surveys are saved with the default name and are not changed by the User
                if survey_id == "recent":
                    survey = RentingSurveyModel.objects.filter(userProf=currProf).order_by('-created').first()
                else:
                    survey = RentingSurveyModel.objects.filter(userProf=currProf).get(id=survey_id)

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
                origins =[]
                for house in housingList:
                    origins.append(house.address)
                destinations = ["Boston, MA"]

                # Can add things to the arugments, like traffic_model, avoid things, depature_time etc
                matrix = gmaps.distance_matrix(origins, destinations,
                                               mode="driving",
                                               units="imperial",
                                               )

                # Generate scores for the homes based on the survey results
                create_house_score(matrix, housingList, survey)

                # Populate template with important important information
                context['survey'] = survey
                context['locations'] = locations
                context['houseList'] = housingList


            except RentingSurveyModel.DoesNotExist:
                context['error_message'].append("Could not retrieve rent survey")
                print("Error, could not find survey id, redirecting back to survey")
                return HttpResponseRedirect(reverse('survey:rentingSurvey'))
        except UserProfile.DoesNotExist:
            context['error_message'].append("Could not find User Profile")

    # fill form with data from database
    form = RentSurveyMini(instance=survey)

    context['form'] = form
    return render(request, 'survey/surveyResult.html', context)
