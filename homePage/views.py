from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import HomePageForm
# Create your views here.


def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HomePageForm(request.POST)
        # check whether it is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to new URL:
            return HttpResponseRedirect('/thanks')
    else:
        form = HomePageForm()

    return render(request, 'homePage/index.html', {'form': form})
