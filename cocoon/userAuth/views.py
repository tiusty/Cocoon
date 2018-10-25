from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from cocoon.userAuth.models import UserProfile, MyUser
from cocoon.survey.models import RentingSurveyModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import LoginUserForm, ApartmentHunterSignupForm, ProfileForm, BrokerSignupForm


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


class TermsOfUse(TemplateView):
    """
    Shows the terms and use page for Cocoon
    """
    template_name = 'userAuth/terms_and_conditions.html'


class SignUpView(TemplateView):
    """
    Redirects user to sign up page which gives them options for what to sign up as
    """
    template_name = 'userAuth/signup.html'


class ApartmentHunterSignupView(CreateView):
    """
    Loads register page for an apartment hunter
    """
    model = MyUser
    form_class = ApartmentHunterSignupForm
    template_name = 'userAuth/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'hunter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('homePage:index'))


class BrokerSignupView(CreateView):
    """
    Loads the sign up page for a broker
    """
    model = MyUser
    form_class = BrokerSignupForm
    template_name = 'userAuth/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'broker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('homePage:index'))


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('homePage:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userAuth/change_password.html', {
        'form': form
    })


def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse('homePage:index'))


@login_required
def user_profile(request):
    context = {
        'error_message': [],
    }

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Updated Account')
            return HttpResponseRedirect(reverse('userAuth:user_profile'))
        else:
            context['error_message'].append("Could not post form, try again")

    # Retrieve data relevant to user
    user_prof = UserProfile.objects.get(user=request.user)
    num_rent_surveys = RentingSurveyModel.objects.filter(user_profile=user_prof).count()
    form = ProfileForm(instance=user_prof.user)

    context['numRentSurveys'] = num_rent_surveys
    context['userProfile'] = user_prof
    context['form'] = form
    return render(request, 'userAuth/user_profile.html', context)


@login_required
def user_surveys(request):
    context = {
        'error_message': [],
    }

    # Retrieve data relevant to user
    profile = UserProfile.objects.get(user=request.user)
    rent_surveys = RentingSurveyModel.objects.filter(user_profile=profile).order_by('-created')
    context['surveys'] = rent_surveys
    return render(request, 'userAuth/user_surveys.html', context)
