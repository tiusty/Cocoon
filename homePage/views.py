from django.shortcuts import render
from homePage.forms import SurveyType
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    form = SurveyType()
    context = {
        'error_message': [],
    }
    if request.method == "POST":
        form = SurveyType(request.POST)
        if form.is_valid():
            survey_type = form.cleaned_data['survey_type']
            if survey_type == "rent":
                return HttpResponseRedirect(reverse('survey:rentingSurvey'))
            elif survey_type == "buy":
                return HttpResponseRedirect('/thanks/')
            else:
                context['error_message'].append("Could not parse radio type")
        else:
            context['error_message'].append("Form not valid, please try again")

    context['form'] = form
    return render(request, 'homePage/index.html', context)
