from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegisterForm, UserCreationForm
# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('userAuth:login'))


def login(request):
    form = LoginForm()
    context = {
        'error_message': [],
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.username, password=form.password)
            if user is not None:
                login(request, user)
                # redirect to success page
                return HttpResponseRedirect(reverse('homePage:index'))
            else:
                # return invalid user
                context['error_message'].append('Unable to login, try again')
        else:
            context['error_message'].append('Unable to login in, refill out the form')
    context['form'] = form
    return render(request, 'userAuth/login.html', context)


def register(request):
    form = RegisterForm()
    context = {
        'error_message': [],
    }
    print('start')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print('was valid')
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            context['error_message'].append('Unable to create user')
    context['form'] = form
    return render(request, 'userAuth/register.html', context)
