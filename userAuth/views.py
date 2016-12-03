from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import LoginForm
# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('userAuth:login'))


def login(request):
    context = {
        'error_message': [],
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to success page
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            # return invalid user
            context['error_message'].append('Unable to login, try again')
    form = LoginForm
    context['form'] = form
    return render(request, 'userAuth/login.html', context)
