from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RentSurvey, BuySurvey
from userAuth.models import UserProfile
from survey.models import survey_types, RentingSurveyModel, default_rent_survey_name


# Create your views here.


# def index(request):
#     form = RentSurvey()
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = RentSurvey(request.POST)
#         # check whether it is valid
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to new URL:
#             return HttpResponseRedirect('/thanks')
#     else:
#         form = RentSurvey()
#
#     return render(request, 'survey/index.html', {'form': form})


def renting_survey(request):
    # Try to set it so if the user is not logged in then it doesn't ask for a name,
    # Or if  no name is provided then it saves it as a temporary survey
    form = RentSurvey()
    context = {
        'error_message': [],
    }
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RentSurvey(request.POST)
        # check whether it is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            rentingSurvey = form.save(commit=False)
            currProf = UserProfile.objects.get(user=request.user)
            # Need to retrieve the current userProfile to link the survye to
            try:
                rentingSurvey.userProf = currProf
                rentingSurvey.survey_type = survey_types.rent.value
                # Try seeing if there is already a recent surey and if there is
                # Then delete it
                try:
                    currRecentSur = RentingSurveyModel.objects.filter(userProf=currProf).filter(name=default_rent_survey_name).delete()
                except RentingSurveyModel.DoesNotExist:
                    print("No surveys to delete")
                rentingSurvey.save()
                # Since commit =False in the save, need to save the many to many fields
                # After saving the form
                form.save_m2m()
                # redirect to new URL:
                return HttpResponseRedirect(reverse('survey:surveyResult',kwargs={'survey_type':"rent"}))
            except currProf.DoesNotExist:
                context['error_message'].append("Could not retrieve the User Profile")
    return render(request, 'survey/rentingSurvey.html', {'form': form})


def buying_survey(request):
    form = BuySurvey()
    return render(request, 'survey/buy.html', {'form':form})


def survey_result(request, survey_type):
    context = {
        'error_message': [],
    }
    if survey_type == "rent":
        try:
            currProf = UserProfile.objects.get(user=request.user)
            try:
                survey = RentingSurveyModel.objects.filter(userProf=currProf).get(name="recent_rent_survey")
            except survey.DoesNotExist:
                context['error_message'].append("Could not retrieve rent survey")
        except currProf.DoesNotExist:
            context['error_message'].append("Could not find User Profile")
    print(survey.home_type)
    context['survey'] = survey
    return render(request, 'survey/surveyResult.html', context)