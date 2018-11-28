from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from cocoon.userAuth.models import UserProfile, MyUser
from cocoon.survey.models import RentingSurveyModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginUserForm, ApartmentHunterSignupForm, ProfileForm, BrokerSignupForm
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator

# Used for email verification
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from .tokens import account_activation_token

# Import Cocoon Modules
from cocoon.signature.models import HunterDocManagerModel
from cocoon.scheduler import views as scheduler_views

# Import Scheduler algorithm
from cocoon.scheduler.clientScheduler.client_scheduler import ClientScheduler


def index(request):
    return HttpResponseRedirect(reverse('userAuth:loginPage'))


@method_decorator(login_required, name='dispatch')
class VisitList(ListView):

    model = RentingSurveyModel
    template_name = 'userAuth/surveys.html'
    context_object_name = 'surveys'

    def get_queryset(self):
        user_prof = get_object_or_404(UserProfile, user=self.request.user)
        return RentingSurveyModel.objects.filter(user_profile=user_prof)

    def get_context_data(self, **kwargs):
        data = super(VisitList, self).get_context_data(**kwargs)
        data['component'] = 'Surveys'
        user_prof = get_object_or_404(UserProfile, user=self.request.user)
        (manager, _) = HunterDocManagerModel.objects.get_or_create(
            user=user_prof.user,
        )

        # Create context to update the html based on the status of the documents
        data['pre_tour_signed'] = manager.is_pre_tour_signed()
        data['pre_tour_forms_created'] = manager.pre_tour_forms_created()

        # Get the user itineraries
        data.update(scheduler_views.get_user_itineraries(self.request))

        return data

    def post(self, request):
        # Run the client scheduler algorithm
        user_prof = get_object_or_404(UserProfile, user=request.user)
        survey = get_object_or_404(RentingSurveyModel, id=self.request.POST['submit-button'], user_profile=user_prof)
        homes_list = []
        for home in survey.visit_list.all():
            homes_list.append(home)

        # Run client_scheduler algorithm
        client_scheduler_alg = ClientScheduler()
        result = client_scheduler_alg.run(homes_list, self.request.user)
        if result:
            messages.info(request, "Itinerary created")
        else:
            messages.warning(request, "Itinerary already exists")
        return HttpResponseRedirect(reverse('userAuth:surveys'))


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

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            return super().get(request, **kwargs)


class ApartmentHunterSignupView(CreateView):
    """
    Loads register page for an apartment hunter
    """
    model = MyUser
    form_class = ApartmentHunterSignupForm
    template_name = 'userAuth/signup_form.html'

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            return super().get(request, **kwargs)

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

        # Create user with commit=False so active can be set to false before saving in the database
        user = form.save(request=self.request)
        login(self.request, user)

        # Send message to next page informing the user of the status of the account
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

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            return super().get(request, **kwargs)

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
        # Create user with commit=False so active can be set to false before saving in the database
        user = form.save(request=self.request)
        login(self.request, user)

        # Send message to next page informing the user of the status of the account
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
        # Try to retrieve the user from the hashed user_id
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # If the user and the token is valid then active the user and log the user in
        user.is_verified = True
        user.save()
        if not request.user.is_authenticated:
            login(request, user)

        # Return the message to inform the user of the status of the account
        messages.info(request, "Thank you for verifying your email")
        return HttpResponseRedirect(reverse('homePage:index'))

    else:
        # Return a message saying the account link was not valid
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
