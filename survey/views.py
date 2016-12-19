from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RentSurvey, BuySurvey


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
    # Or if  no name is provided then it saves it as a temperary survey
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
            # ...
            # redirect to new URL:
            return HttpResponseRedirect('/thanks')
    print(form)
    return render(request, 'survey/rentingSurvey.html', {'form': form})


def buying_survey(request):
    form = BuySurvey()
    return render(request, 'survey/buy.html', {'form':form})