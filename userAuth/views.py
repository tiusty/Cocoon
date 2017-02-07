from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from userAuth.models import UserProfile
from survey.models import RentingSurveyModel, RentingDesintations

from .forms import LoginUserForm, RegisterForm, ProfileForm
# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('userAuth:loginPage'))


def loginPage(request):
    form = LoginUserForm()
    context = {
        'error_message': [],
    }
    if request.method == 'POST':
        form = LoginUserForm(request, request.POST)
        if form.is_valid():
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
            # The email address is used as the username
            form.save()
            # Try to have the user automatically log in but for now go back to login page
            return HttpResponseRedirect(reverse('userAuth:loginPage'))
        else:
            context['error_message'].append('Unable to create user')
    context['form'] = form
    return render(request, 'userAuth/register.html', context)


def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse('userAuth:loginPage'))


def ProfilePage(request, defaultPage="profile"):
    context = {
        'error_message': [],
    }

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
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
        elif defaultPage == "buySurvey":
            context['defaultProfile'] = 2
        else:
            context['defaultProfile'] = 0

    else:
        return HttpResponseRedirect(reverse('userAuth:loginPage'))

    rentSurveys = RentingSurveyModel.objects.filter(userProf=userProfile).order_by('-created')[:50]
    context['numRentSurveys'] = rentSurveys.count()
    context['numBuySurveys'] = 0
    context['surveys'] = rentSurveys
    form = ProfileForm(instance=userProfile.user)
    context['form'] = form
    return render(request, 'userAuth/profilePage.html', context)
