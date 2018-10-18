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

# Used for email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage


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
            context['error_message'].append("Could not login. Please verify your email if you haven't yet")

    context['form'] = form
    return render(request, 'userAuth/login.html', context)


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
        """
        When the hunter creates an account make sure to set the user.is_active = false
            and then send an email to their account so they can validate the account
        :param form: (ApartmentHunterSignupForm) -> The hunter signup form with their info
        :return: (HttpResponseRedirect) -> Send them to the home page with the valid message
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your Cocoon Account'
        message = render_to_string(
            'userAuth/email/account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.info(self.request, "Please confirm your email address to complete registration. "
                                    "Make sure to check the spam folder")
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
        """
        When the Broker creates an account make sure to set the user.is_active = false
            and then send an email to their account so they can validate the account
        :param form: (BrokerSignupForm) -> The broker signup form with their info
        :return: (HttpResponseRedirect) -> Send them to the home page with the valid message
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your Cocoon Account'
        message = render_to_string(
            'userAuth/email/account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.info(self.request, "Please confirm your email address to complete registration. "
                                    "Make sure to check the spam folder")
        return HttpResponseRedirect(reverse('homePage:index'))


def activate_account(request, uidb64, token):
    """
    Given a uidb and token from an email authentication link make sure the token etc is valid
        and then if it is then activate the user account and login them in
    :param request: (request) -> The http request
    :param uidb64: (string) -> The user id hashed
    :param token: (string) -> The token that validates the link to the user account
    :return: (httpredirect) -> To the home page
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.info(request, "Thank you for verifying your email")
        return HttpResponseRedirect(reverse('homePage:index'))
    else:
        messages.error(request, "The activation link is invalid")
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
