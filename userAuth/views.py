from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import LoginUserForm, RegisterForm
# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('userAuth:login'))


def loginPage(request):
    form = LoginUserForm()
    context = {
        'error_message': [],
    }
    if request.method == 'POST':
        form = LoginUserForm(request, request.POST)
        print("here")
        print(form.is_bound)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)
            if user is not None:
                login(request, user)
                # redirect to success page
                return HttpResponseRedirect(reverse('homePage:index'))
            else:
                # return invalid user
                context['error_message'].append('Unable to login in with Email/Password combo')
        else:
            context['error_message'].append('Unable to login in, refill out the form')
    context['form'] = form
    return render(request, 'userAuth/login.html', context)


def registerPage(request):
    form = RegisterForm()
    context = {
        'error_message': [],
    }
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form)
            # The email address is used as the username
            form.save()
            print('was valid')
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            context['error_message'].append('Unable to create user')
    context['form'] = form
    return render(request, 'userAuth/register.html', context)
