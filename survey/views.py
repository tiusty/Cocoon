from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import InitialSurvey

# Create your views here.


def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InitialSurvey(request.POST)
        # check whether it is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to new URL:
            return HttpResponseRedirect('/thanks')
    else:
        form = InitialSurvey()

    return render(request, 'survey/index.html', {'form': form})


