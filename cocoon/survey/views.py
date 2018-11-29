# Import Python Modules
import json

# Import Django modules
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
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

# Import Scheduler algorithm
from cocoon.scheduler.clientScheduler.client_scheduler import ClientScheduler

# Import Itinerary model
from cocoon.survey.serializers import RentSurveySerializer

# import scheduler views
from cocoon.scheduler import views as scheduler_views

from cocoon.userAuth.forms import ApartmentHunterSignupForm

# Rest Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response


class RentingSurvey(CreateView):
    model = RentingSurveyModel
    form_class = RentSurveyForm
    template_name = 'survey/rentingSurvey.html'

    def get_context_data(self, **kwargs):
        """
        Adds the TenantFormSet, and the user creation form to the context
        """
        data = super(RentingSurvey, self).get_context_data(**kwargs)
        data['component'] = 'survey'
        data['props'] = 'test'

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

        The Rent Algorithm is only run when the request is not POST (i.e loading the page)
            or when the form is invalid (i.e to reload the page with errors)
            On form_valid it is not rendered because it will be redirected back to the page
                and thus the get method will run the algorithm (thus prevents running it twice)

        kwargs:
            invalid_form: -> Determines if the get_context_data is being called from form_invalid
        """
        data = super(RentingResultSurvey, self).get_context_data(**kwargs)

        form_invalid = kwargs.pop('invalid_form', False)
        # Only run the Algorithm if the form was either invalid or it was a get method
        #   We don't want to run the algorithm on form valid
        if form_invalid or not self.request.POST:
            rent_algorithm = RentAlgorithm()
            rent_algorithm.run(self.object)
            data['houseList'] = [x for x in rent_algorithm.homes[:25] if x.percent_score() >= 0]

        # If the request is a post, then populate the tenant form set
        if self.request.POST:
            data['tenants'] = TenantFormSetResults(self.request.POST, instance=self.object)
        # Otherwise if it is just a get, then just create a new form set
        else:
            data['tenants'] = TenantFormSetResults(instance=self.object)

        favorite_homes = self.object.favorites.all()
        data['user_favorite_houses'] = favorite_homes
        return data

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form, invalid_form=True))

    def form_valid(self, form):
        context = self.get_context_data()
        tenants = context['tenants']

        # Makes sure that the tenant form is valid before saving
        if tenants.is_valid():

            user = self.request.user

            # Save the survey
            with transaction.atomic():
                form.instance.user_profile = get_object_or_404(UserProfile, user=user)
                survey = form.save()

            # Now save the the tenants
            tenants.instance = survey
            tenants.save()
        else:
            # If there are any errors then the form is not valid
            return self.form_invalid(form=form)
        messages.add_message(self.request, messages.SUCCESS, "Survey Updated!")
        return HttpResponseRedirect(reverse('survey:rentSurveyResult',
                                            kwargs={"survey_url": self.object.url}))


class VisitList(ListView):

    model = RentingSurveyModel
    template_name = 'survey/visitList.html'
    context_object_name = 'surveys'

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return RentingSurveyModel.objects.filter(user_profile=user_profile)

    def get_context_data(self, **kwargs):
        data = super(VisitList, self).get_context_data(**kwargs)
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        (manager, _) = HunterDocManagerModel.objects.get_or_create(
            user=user_profile.user,
        )

        # Since the page is loading, update all the signed documents to see if the status has changed
        manager.update_all_is_signed()

        # Create context to update the html based on the status of the documents
        data['pre_tour_signed'] = manager.is_pre_tour_signed()
        data['pre_tour_forms_created'] = manager.pre_tour_forms_created()

        # Get the user itineraries
        data.update(scheduler_views.get_user_itineraries(self.request))

        return data

    def post(self, request, *args, **kwargs):
        # Run the client scheduler algorithm
        user_profile = get_object_or_404(UserProfile, user=request.user)
        survey = get_object_or_404(RentingSurveyModel, id=self.request.POST['submit-button'], user_profile=user_profile)
        homes_list = []
        for home in survey.visit_list.all():
            homes_list.append(home)

        # Run client_scheduler algorithm
        client_scheduler_alg = ClientScheduler()
        client_scheduler_alg.calculate_duration(homes_list, self.request.user)
        messages.info(request, "Itinerary created")
        return HttpResponseRedirect(reverse('survey:visitList'))


class RentSurveyViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = RentSurveySerializer

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return RentingSurveyModel.objects.filter(user_profile=user_profile)

    def update(self, request, *args, **kwargs):
        """
        Updates a survey with one of the option listed by the kwargs['types']

        :param request:
        :param args:
        :param kwargs:
            Expects:
                home_id: (int) -> The int of the home to toggle
                type: (string) -> The type of update that is occurring
                    One of:
                        visit_toggle: A visit list home is being toggled
                        favorite_toggle: A favorite home is being toggled
                        survey_delete: A survey is being deleted
        :return:
        """

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

        # Retrieve the associated survey with the request
        survey = get_object_or_404(RentingSurveyModel, user_profile=user_profile, pk=pk)

        # Case if a visit list home is being removed or added
        if 'visit_toggle' in self.request.data['type']:

            # If the home already exists in the visit list then remove it
            try:
                home = survey.visit_list.get(id=self.request.data['home_id'])
                survey.visit_list.remove(home)

            # if the home does not exist in the vist list then add it
            except RentDatabaseModel.DoesNotExist:
                try:
                    home = RentDatabaseModel.objects.get(id=self.request.data['home_id'])
                    survey.visit_list.add(home)
                except RentDatabaseModel.DoesNotExist:
                    pass

        # Case if a favorite home is being removed or added
        elif 'favorite_toggle' in self.request.data['type']:
            # If the home exists in the favorite list already then remove it
            try:
                home = survey.favorites.get(id=self.request.data['home_id'])
                survey.favorites.remove(home)

            # If the home does not exist in the favorite list then add it
            except RentDatabaseModel.DoesNotExist:
                try:
                    home = RentDatabaseModel.objects.get(id=self.request.data['home_id'])
                    survey.favorites.add(home)
                except RentDatabaseModel.DoesNotExist:
                    pass

        # Case if a survey is being deleted
        elif 'survey_delete' in self.request.data['type']:
            # Delete the current survey
            survey.delete()

            # Return a list of all the current surveys
            return self.list(request, args, kwargs)

        # Returns the survey that was updated
        serializer = RentSurveySerializer(survey)
        return Response(serializer.data)


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
            survey_id = request.POST.get('survey')
            # Retrieve the house associated with that id
            try:
                house = RentDatabaseModel.objects.get(id=house_id)
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    # If the house is already in the database then remove it and return 0
                    # Which means that it is no longer in the favorites
                    try:
                        survey = RentingSurveyModel.objects.filter(user_profile=user_profile).get(id=survey_id)
                        if survey.favorites.filter(id=house_id).exists():
                            survey.favorites.remove(house)
                            return HttpResponse(json.dumps({"result": "0"}),
                                                content_type="application/json",
                                                )
                        # If the  house is not in the Many to Many then add it and
                        # return 1 which means it is currently in the favorites
                        else:
                            survey.favorites.add(house)
                            return HttpResponse(json.dumps({"result": "1"}),
                                                content_type="application/json",
                                                )
                    except RentingSurveyModel.DoesNotExist:
                        return HttpResponse(json.dumps({"result": "Survey Does not exist"}),
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
            house_id = request.POST.get('visit_id')
            survey_id = request.POST.get('survey')
            try:
                house = RentDatabaseModel.objects.get(id=house_id)
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    try:
                        survey = RentingSurveyModel.objects.filter(user_profile=user_profile).get(id=survey_id)
                        if survey.visit_list.filter(id=house_id).exists():
                            survey.visit_list.remove(house)
                            return HttpResponse(json.dumps({"result": "0"}),
                                                content_type="application/json",
                                                )
                        # If the  house is not in the Many to Many then add it and
                        # return 1 which means it is currently in the favorites
                        else:
                            survey.visit_list.add(house)
                            return HttpResponse(json.dumps({"result": "1"}),
                                                content_type="application/json",
                                                )
                    except RentingSurveyModel.DoesNotExist:
                        return HttpResponse(json.dumps({"result": "Survey Does not exist"}),
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
