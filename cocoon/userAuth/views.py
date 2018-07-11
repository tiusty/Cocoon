from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from cocoon.userAuth.models import UserProfile
from cocoon.survey.models import RentingSurveyModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginUserForm, RegisterForm, ProfileForm
# Create your views here.

#import global config values
from config.settings.Global_Config import creation_key_value


def index(request):
    return HttpResponseRedirect(reverse('userAuth:loginPage'))


def loginPage(request):
    form = LoginUserForm()
    context = {
        'error_message': [],
    }

    # If the user is already authenticated them redirect to index page
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homePage:index'))

    elif request.method == 'POST':
        form = LoginUserForm(request, request.POST)
        if form.is_valid():
            if not form.cleaned_data['remember']:
                request.session.set_expiry(0)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
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
            if form.cleaned_data['creation_key'] == creation_key_value:
                # The email address is used as the username
                form.save()
                # Try to have the user automatically log in but for now go back to login page
                messages.add_message(request, messages.SUCCESS, 'Successfully registered user')
                return HttpResponseRedirect(reverse('userAuth:loginPage'))
            else:
                form.add_error('creation_key', 'Creation key wrong')
                context['error_message'].append("Creation key wrong")
        else:
            context['error_message'].append('Unable to create user')
    context['form'] = form
    return render(request, 'userAuth/register.html', context)


def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse('homePage:index'))


@login_required
def ProfilePage(request, defaultPage="profile"):
    context = {
        'error_message': [],
    }

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Updated Account')
            return HttpResponseRedirect(reverse('userAuth:profilePage',
                                                kwargs={'defaultPage': "profile"}))
        else:
            context['error_message'].append("Could not post form, try again")
    if request.user.is_authenticated():
        userProfile = UserProfile.objects.get(user=request.user)
        context['userProfile'] = userProfile
        if defaultPage == "profile":
            context['defaultProfile'] = 0
        elif defaultPage == "rentSurvey":
            context['defaultProfile'] = 1
        # for now since buy survey is not implemented, just have it load the rent survey
        elif defaultPage == "buySurvey":
            context['defaultProfile'] = 1
        elif defaultPage == "favorites":
            context['defaultProfile'] = 3
        else:
            context['defaultProfile'] = 0
        context['favorites'] = userProfile.favorites.all()

    else:
        messages.add_message(request,messages.ERROR, "User is not authenticated")
        return HttpResponseRedirect(reverse('userAuth:loginPage'))

    rent_surveys = RentingSurveyModel.objects.filter(user_profile_survey=userProfile).order_by('-created_survey')[:50]
    context['numRentSurveys'] = rent_surveys.count()
    context['numBuySurveys'] = 0
    context['surveys'] = rent_surveys
    form = ProfileForm(instance=userProfile.user)
    context['form'] = form
    return render(request, 'userAuth/profilePage.html', context)

@login_required
def SurveyPage(request, defaultPage="rentSurvey"):
    context = {
        'error_message': [],
    }

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Updated Account')
            return HttpResponseRedirect(reverse('userAuth:profilePage',
                                                kwargs={'defaultPage': "profile"}))
        else:
            context['error_message'].append("Could not post form, try again")
    if request.user.is_authenticated():
        userProfile = UserProfile.objects.get(user=request.user)
        context['userProfile'] = userProfile
        if defaultPage == "profile":
            context['defaultProfile'] = 0
        elif defaultPage == "rentSurvey":
            context['defaultProfile'] = 1
        # for now since buy survey is not implemented, just have it load the rent survey
        elif defaultPage == "buySurvey":
            context['defaultProfile'] = 1
        elif defaultPage == "favorites":
            context['defaultProfile'] = 3
        else:
            context['defaultProfile'] = 0
        context['favorites'] = userProfile.favorites.all()

    else:
        messages.add_message(request, messages.ERROR, "User is not authenticated")
        return HttpResponseRedirect(reverse('userAuth:loginPage'))

    rent_surveys = RentingSurveyModel.objects.filter(user_profile_survey=userProfile).order_by('-created_survey')[:50]
    context['numRentSurveys'] = rent_surveys.count()
    context['numBuySurveys'] = 0
    context['surveys'] = rent_surveys
    form = ProfileForm(instance=userProfile.user)
    context['form'] = form
    return render(request, 'userAuth/mySurveys.html', context)