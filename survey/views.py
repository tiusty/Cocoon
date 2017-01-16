from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RentSurvey, BuySurvey, DestinationForm, RentSurveyMini
from userAuth.models import UserProfile
from survey.models import survey_types, RentingSurveyModel, default_rent_survey_name
from houseDatabase.models import RentDatabase

# Create your views here.
def renting_survey(request):
    # Try to set it so if the user is not logged in then it doesn't ask for a name,
    # Or if  no name is provided then it saves it as a temporary survey
    form = RentSurvey()
    formDest = DestinationForm()
    context = {
        'error_message': [],
    }
    if request.method == 'POST':

        # first validating Destination form
        formDest = DestinationForm(request.POST)
        # create a form instance and populate it with data from the request:
        form = RentSurvey(request.POST)

        # Check to see if the desinations are valid
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
                    # Then delete it
                    try:
                        surveyName = default_rent_survey_name
                        currRecentSur = RentingSurveyModel.objects.filter(userProf=currProf).filter(name=surveyName).delete()
                    except RentingSurveyModel.DoesNotExist:
                        print("No surveys to delete")
                    rentingSurvey.save()
                    # Since commit =False in the save, need to save the many to many fields
                    # After saving the form
                    form.save_m2m()

                    try:
                        survey = RentingSurveyModel.objects.filter(userProf=currProf).get(name=surveyName)
                        destinations = formDest.save(commit=False)
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
            if not form.is_valid():
                context['error_message'].append("The normal form is also not valid")
            context['error_message'].append("Destination form is not valid")
    return render(request, 'survey/rentingSurvey.html', {'form': form, 'formDest':formDest})


def buying_survey(request):
    form = BuySurvey()
    return render(request, 'survey/buyingSurvey.html', {'form':form})


# Switch it so when no survey is specified it just grabs the recent survey, otherwise it grabs
# the survey that is specified


##### Things that need to be worked on
# Think of a better way of figuring out which survey is needed.
# One way is to hvae a function default to the deafult survey name if no survey is specified in the url
# if something is specified in the URL then it loads that survey if that id matches an id of that user
# This fucntion fails if the survey doesn't have the default name survey, aka if someone changes the name of the most
#most recent survey. What should happen is if someone tries to change the name of the most recent survey then instead,
# createa new model with the same data so there is always a recent survey
# Commenting this out for now because of the complications
# def survey_result(request, survey_type):
#     context = {
#         'error_message': [],
#     }
#     form = RentSurveyMini()
#     if request.method == 'POST':
#         try:
#             currProf = UserProfile.objects.get(user=request.user)
#             try:
#                 # Need to handle case
#                 survey = RentingSurveyModel.objects.filter(userProf=currProf).get(name=default_rent_survey_name)
#                 form = RentSurveyMini(request.POST, instance=survey)
#                 if form.is_valid():
#                     if form.cleaned_data['name'] != default_rent_survey_name:
#                         form.instance
#                     form.save()
#                 else:
#                     context['error_message'].append("The survey was POSTed incorrectly")
#             except RentingSurveyModel.DoesNotExist:
#                 context['error_message'].append("Survey does not exist")
#         except UserProfile.DoesNotExist:
#             context['error_message'].append("User profile doesn't exist")
#         # Now add saving the form data to the survey. Make sure to filter by user so someone could not save data
#         # to another user
#         # Then once the survey is saved, do a redirect to the survey to redisplay new results
#
#     if survey_type == "rent":
#         try:
#             currProf = UserProfile.objects.get(user=request.user)
#             try:
#                 survey = RentingSurveyModel.objects.filter(userProf=currProf).get(name="recent_rent_survey")
#                 homeTypes = []
#                 for home in survey.home_type.all():
#                     homeTypes.append(home.homeType)
#                 housingList = RentDatabase.objects.filter(price__range=(survey.minPrice, survey.maxPrice))\
#                     .filter(home_type__in=homeTypes)
#                 locations = survey.rentingdesintations_set.all()
#                 context['survey'] = survey
#                 context['locations'] = locations
#                 context['houseList'] = housingList
#             except RentingSurveyModel.DoesNotExist:
#                 context['error_message'].append("Could not retrieve rent survey")
#         except UserProfile.DoesNotExist:
#             context['error_message'].append("Could not find User Profile")
#
#     context['form'] = form
#     return render(request, 'survey/surveyResult.html', context)

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
                # Need to handle case
                survey = RentingSurveyModel.objects.filter(userProf=currProf).get(id=survey_id)
                form = RentSurveyMini(request.POST, instance=survey)
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
        # Now add saving the form data to the survey. Make sure to filter by user so someone could not save data
        # to another user
        # Then once the survey is saved, do a redirect to the survey to redisplay new results

    #
    if survey_type == "rent":
        try:
            currProf = UserProfile.objects.get(user=request.user)
            try:
                if survey_id == "recent":
                    survey = RentingSurveyModel.objects.filter(userProf=currProf).order_by('-created').first()
                else:
                    survey = RentingSurveyModel.objects.filter(userProf=currProf).get(id=survey_id)
                homeTypes = []
                for home in survey.home_type.all():
                    homeTypes.append(home.homeType)
                housingList = RentDatabase.objects.filter(price__range=(survey.minPrice, survey.maxPrice))\
                    .filter(home_type__in=homeTypes)
                locations = survey.rentingdesintations_set.all()
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