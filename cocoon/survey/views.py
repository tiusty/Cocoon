# Import Python Modules
import json
# from silk.profiling.profiler import silk_profile

# Import Django modules
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.db import transaction
from django.contrib.auth import login

# Import Signatures modules
from cocoon.signature.models import HunterDocManagerModel

# Import House Database modules
from cocoon.houseDatabase.models import RentDatabaseModel

# Import User Auth modules
from cocoon.userAuth.models import UserProfile

# Import Survey algorithm modules
from cocoon.survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from cocoon.survey.models import RentingSurveyModel
from cocoon.survey.forms import RentSurveyForm, TenantFormSet, TenantFormSetResults, RentSurveyFormMini

from cocoon.userAuth.forms import ApartmentHunterSignupForm


class RentingSurvey(CreateView):
    model = RentingSurveyModel
    form_class = RentSurveyForm
    template_name = 'survey/rentingSurvey.html'

    def get_context_data(self, **kwargs):
        """
        Adds the TenantFormSet, and the user creation form to the context
        """
        data = super(RentingSurvey, self).get_context_data(**kwargs)

        # If the request is a post, then populate the tenant form set
        if self.request.POST:

            # This is a hack to remove the forms that are not desired by the user
            #   Basically the number of tenants is read from the input, then
            #   all the forms that are beyond the desired amount of tenants
            #   is deleted from the request.POST (a copy of it)
            request_post = self.request.POST.copy()
            for x in range(int(request_post['number_of_tenants']), 5):
                for field in self.request.POST:
                    if 'tenants-' + str(x) in field:
                        del request_post[field]
            self.request.POST = request_post
            # Populate the formset with the undesired formsets stripped away
            data['tenants'] = TenantFormSet(self.request.POST)

            # If the user is not signed in then add then create the signup form with
            #   the request.POST elements
            if not self.request.user.is_authenticated():
                data['user_creation'] = ApartmentHunterSignupForm(self.request.POST)

            # Determine the desired amount of tenants from the request.POST
            data['num_of_tenants'] = int(self.request.POST['number_of_tenants'])

        # Otherwise if it is just a get, then just create a new form set
        else:

            # Create a blank Tenant form set
            data['tenants'] = TenantFormSet()

            # The default value is 1
            data['num_of_tenants'] = 1

            # If the user is not logged in then generate a signup form
            if not self.request.user.is_authenticated():
                data['user_creation'] = ApartmentHunterSignupForm()
        return data

    def form_valid(self, form):
        """
        Runs if the RentSurveyForm is valid
        :param form: (RentSurveyForm) -> The form associated with the page
        """
        context = self.get_context_data()
        tenants = context['tenants']

        does_user_signup = False
        sign_up_form_valid = True
        user_signup = None

        # Determines if there is a signup form associated with the request
        # If there is then the signup form must also be valid
        if 'user_creation' in context:
            does_user_signup = True
            user_signup = context['user_creation']
            if not user_signup.is_valid():
                sign_up_form_valid = False

        # Makes sure that the tenant form and the signup form are valid before saving
        if tenants.is_valid() and sign_up_form_valid:

            user = self.request.user

            # If the user is signing up then save that form and return the user to log them in
            if does_user_signup:
                user = user_signup.save(request=self.request)
                login(self.request, user)

            # Save the rent survey
            with transaction.atomic():
                form.instance.user_profile = get_object_or_404(UserProfile, user=user)

                # Creates a the survey name based on the people in the roommate group
                survey_name = "Roommate Group:"
                counter = 1
                # Depending on whether it is the last/first roommate then the formatting of the string is different
                for tenant in tenants:

                    # If only the user
                    if counter is 1 and counter is context['num_of_tenants']:
                        survey_name = survey_name + " Just Me"
                        break

                    # Write me for the user as the first person in the roomate group
                    elif counter is 1:
                        survey_name = survey_name + " Me,"

                    # End condition for the last roomate
                    elif counter >= context['num_of_tenants']:
                        survey_name = survey_name + " and {0}".format(tenant.cleaned_data['first_name'])
                        break

                    # Adds another roommate to the group
                    else:
                        survey_name = survey_name + ", {0}".format(tenant.cleaned_data['first_name'])

                    counter = counter + 1

                # Set the form name
                form.instance.name = survey_name

                # Now the form can be saved
                survey = form.save()

            # Now save the the tenants
            tenants.instance = survey
            tenants.save()

        else:
            # If there is an error then re-render the survey page
            return self.render_to_response(self.get_context_data(form=form))

        # Redirect to survey results page on success
        return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                            kwargs={"survey_url": survey.url}))


class RentingResultSurvey(UpdateView):
    model = RentingSurveyModel
    form_class = RentSurveyFormMini
    template_name = 'survey/surveyResultRent.html'
    slug_field = 'url'
    slug_url_kwarg = 'survey_url'
    context_object_name = 'survey'

    def get(self, request, **kwargs):
        """
        Add a message to the user whenever the page is loaded
        """
        messages.add_message(request, messages.INFO, "We've scoured the market to pick your personalized short list of "
                                                     "the best places, now it's your turn to pick your favorites")
        return super().get(request, **kwargs)

    def get_form_kwargs(self):
        """
        Adds the user to the kwargs of the form so it can be accessed in validation
        """
        kwargs = super(RentingResultSurvey, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        """
        The survey must be associated with the currently logged in user
        """
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return RentingSurveyModel.objects.filter(user_profile=user_profile)

    def get_context_data(self, **kwargs):
        """
        Adds the tenant form context
        Also runs the algorithm and returns the homes to the template
        """
        data = super(RentingResultSurvey, self).get_context_data(**kwargs)

        # If the request is a post, then populate the tenant form set
        if self.request.POST:
            data['tenants'] = TenantFormSetResults(self.request.POST, instance=self.object)

        # Otherwise if it is just a get, then just create a new form set
        else:
            data['tenants'] = TenantFormSetResults(instance=self.object)
            # only run the algorithm if it wasn't a POST method
            #   We don't want to run the algorithm on form submit
            rent_algorithm = RentAlgorithm()
            rent_algorithm.run(self.object)
            data['houseList'] = [x for x in rent_algorithm.homes[:25] if x.percent_score() >= 0]
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tenants = context['tenants']

        # Makes sure that the tenant form is valid before saving
        if tenants.is_valid():

            user = self.request.user

            # Save the survey
            with transaction.atomic():
                form.instance.user_profile = get_object_or_404(UserProfile, user=user)
                object = form.save()

            # Now save the the tenants
            tenants.instance = object
            tenants.save()
        else:
            # If there is an error then re-render the survey page
            return self.render_to_response(self.get_context_data(form=form))

        messages.add_message(self.request, messages.SUCCESS, "Survey Updated!")
        return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                            kwargs={"survey_url": self.object.url}))


@login_required
def visit_list(request):

    context = views.get_user_itineraries(request)
    context['error_message'] = []

    # Retrieve the models
    user_profile = get_object_or_404(UserProfile, user=request.user)
    (manager, _) = HunterDocManagerModel.objects.get_or_create(
        user=user_profile.user,
    )

    # Since the page is loading, update all the signed documents to see if the status has changed
    manager.update_all_is_signed()

    # Create context to update the html based on the status of the documents
    context['pre_tour_signed'] = manager.is_pre_tour_signed()
    context['pre_tour_forms_created'] = manager.pre_tour_forms_created()

    return render(request, 'survey/visitList.html', context)


#######################################################
# Ajax Requests below
#############################################################

# This is used for ajax request to set house favorites
@login_required
def set_favorite(request):
    """
    Ajax request that sets a home as a favorite. This function just toggles the homes.
    Therefore, if the home is requested, if it already existed in the database as a favorite
    Then it removes it from the favorites. If it was not in the database as a favorite then it favorites it. The return
    value is the current state of the house after toggling the home. It returns a 0 if the home is
    not in the home and returns a 1 if the home is a favorite
    :param request: The HTTP request
    :return: An HTTP response which returns a JSON
        0- house not in favorites
        1- house in favorites
        else:
            - the error message
    """
    if request.method == 'POST':
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            house_id = request.POST.get('fav')
            # Retrieve the house associated with that id
            try:
                house = RentDatabaseModel.objects.get(id=house_id)
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    # If the house is already in the database then remove it and return 0
                    # Which means that it is no longer in the favorites
                    if user_profile.favorites.filter(id=house_id).exists():
                        user_profile.favorites.remove(house)
                        return HttpResponse(json.dumps({"result": "0"}),
                                            content_type="application/json",
                                            )
                    # If the  house is not in the Many to Many then add it and
                    # return 1 which means it is currently in the favorites
                    else:
                        user_profile.favorites.add(house)
                        return HttpResponse(json.dumps({"result": "1"}),
                                            content_type="application/json",
                                            )
                except UserProfile.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                        content_type="application/json",
                                        )
            # Return an error is the house cannot be found
            except RentDatabaseModel.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve house"}),
                                    content_type="application/json",
                                    )


@login_required
def delete_survey(request):
    """
    Deletes the given Survey passed by the User.
    It only deletes the survey if the survey corresponds to the given user.
    Always returns to the profile page of the renting survey
    :param request: HTTP request object
    :return:
        0 if the survey was successfully deleted
        error message if the survey was not successfully deleted
    """
    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            survey_id = request.POST.get('survey')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    survey_delete = user_profile.rentingsurveymodel_set.get(id=survey_id)
                    survey_delete.delete()
                    return HttpResponse(json.dumps({"result": "0"}),
                                        content_type="application/json",
                                        )

                except RentingSurveyModel.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Survey"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "Method Not POST"}),
                            content_type="application/json",
                            )


@login_required
def set_visit_house(request):
    """
    This ajax function adds a house to the users visit list
    :param request: Http request
    :return: 1 means the home has successfully added
    """

    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            home_id = request.POST.get('visit_id')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    home = RentDatabaseModel.objects.get(id=home_id)
                    user_profile.visit_list.add(home)
                    return HttpResponse(json.dumps({"result": "1",
                                                    "homeId": home_id}),
                                        content_type="application/json", )
                except RentDatabaseModel.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Home"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "Method Not POST"}),
                            content_type="application/json",
                            )


@login_required
def delete_visit_house(request):
    """
    This ajax function removes a house from the users visit list
    :param request: Http request
    :return: 0 means the home was successfully removed
    """

    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            home_id = request.POST.get('visit_id')
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    home = RentDatabaseModel.objects.get(id=home_id)
                    user_profile.visit_list.remove(home)
                    return HttpResponse(json.dumps({"result": "0"}),
                                        content_type="application/json", )
                except RentDatabaseModel.DoesNotExist:
                    return HttpResponse(json.dumps({"result": "Could not retrieve Home"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "Method Not POST"}),
                            content_type="application/json",
                            )


@login_required
def check_pre_tour_documents(request):
    """
    This function is a ajax request that either sends the documents if they are not created
        or will check the status of the documents if they are already sent
    :param request: The HTTP request
    :return: An HTTP response which returns a JSON
        result:
            0- failures
            1- success - Pre-tour document is not signed but is sent (either just sent or already had been sent)
            2 - success - Pre-tour document signed
        message:
            - the message associated with the request
    """
    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    doc_manager = user_profile.user.doc_manager
                    if not doc_manager.pre_tour_forms_created():
                        if doc_manager.create_pre_tour_documents():
                            return HttpResponse(json.dumps({"result": "1",
                                                            "message": "Document Created"}),
                                                content_type="application/json", )
                        else:
                            return HttpResponse(json.dumps({"result": "1",
                                                            "message": "Document already exists"}),
                                                content_type="application/json", )
                    else:
                        doc_manager.update_all_is_signed()
                        if doc_manager.is_pre_tour_signed():
                            return HttpResponse(json.dumps({"result": "2",
                                                            "message": "Document signed!"}),
                                                content_type="application/json", )
                        else:
                            return HttpResponse(json.dumps({"result": "1",
                                                            "message": "Document still not signed"}),
                                                content_type="application/json", )

                except HunterDocManagerModel.DoesNotExist:
                    return HttpResponse(json.dumps({
                        "result": "0",
                        "message": "Could not retrieve doc_manager"}),
                                        content_type="application/json",
                                        )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "0",
                                                "message": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "0",
                                            "message": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "0",
                                        "message": "Method Not POST"}),
                            content_type="application/json",
                            )


@login_required
def resend_pre_tour_documents(request):
    """
    This ajax request will resend the pre-tour documents to the users email
    :param request: The HTTP request
    :return: An HTTP response which returns a JSON
        result:
            0- failures
            1- success - The document was resent to the user
        message:
            - the message associated with the request
    """
    if request.method == "POST":
        # Only care if the user is authenticated
        if request.user.is_authenticated():
            # Get the id that is associated with the AJAX request
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                try:
                    doc_manager = user_profile.user.doc_manager
                    if doc_manager.resend_pre_tour_documents():
                        return HttpResponse(json.dumps({"result": "1",
                                                        "message": "Document resent"}),
                                            content_type="application/json", )
                    else:
                        return HttpResponse(json.dumps({"result": "0",
                                                        "message": "Document not resent"}),
                                            content_type="application/json", )

                except HunterDocManagerModel.DoesNotExist:
                    return HttpResponse(json.dumps({
                        "result": "0",
                        "message": "Could not retrieve doc_manager"}),
                        content_type="application/json",
                    )
            except UserProfile.DoesNotExist:
                return HttpResponse(json.dumps({"result": "0",
                                                "message": "Could not retrieve User Profile"}),
                                    content_type="application/json",
                                    )
        else:
            return HttpResponse(json.dumps({"result": "0",
                                            "message": "User not authenticated"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "0",
                                        "message": "Method Not POST"}),
                            content_type="application/json",
                            )
