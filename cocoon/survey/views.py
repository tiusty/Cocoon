# Import Django modules
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Import Survey algorithm modules
from .cocoon_algorithm.rent_algorithm import RentAlgorithm
from .models import RentingSurveyModel
from .forms import RentSurveyForm, RentSurveyFormEdit, TenantFormSet, TenantFormSetJustNames
from .survey_helpers.save_polygons import save_polygons
from .serializers import HomeScoreSerializer, RentSurveySerializer, SurveySubscribeSerializer
from .constants import NUMBER_OF_HOMES_RETURNED

# Cocoon Modules
from cocoon.userAuth.forms import ApartmentHunterSignupForm
from cocoon.userAuth.models import UserProfile
from cocoon.houseDatabase.models import RentDatabaseModel
from cocoon.userAuth.forms import LoginUserForm

# Rest Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .tasks import compute_survey_result_iteration_task

# Load the logger
import logging
logger = logging.getLogger(__name__)


class RentingSurveyTemplate(TemplateView):
    """
    Template to load the react for the rent survey page
    """

    template_name = "survey/rentForm.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['component'] = RentingSurveyTemplate.__name__
        return data


@method_decorator(login_required, name='dispatch')
class RentingResultTemplate(DetailView):
    """
    Detail view to load the react for the rent result page

    The reason why the detail view is used is to cause a 404 if the user
        tries to load a survey that doesn't exist or they don't own
    """

    template_name = "survey/rentResult.html"
    model = RentingSurveyModel
    slug_field = 'url'
    slug_url_kwarg = 'survey_url'

    def get_queryset(self):
        """
        The survey must be associated with the currently logged in user
        """
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return retrieve_survey_queryset(user_profile)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['component'] = RentingResultTemplate.__name__
        return data


class RentSurveyViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                        mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = RentSurveySerializer

    def get_serializer_context(self):
        """
        Gets the context data for the serializer so that broker accounts get the information regarding
            the home
        """
        return {'user': self.request.user}

    def get_permissions(self):
        """
        Dynamically get permissions because we only allow the user to not be authenticated on the
            create method
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return retrieve_survey_queryset(user_profile)

    def list(self, request, *args, **kwargs):
        """
        When the surveys are being listed, only return the surveys that belong to the user.
        This is needed because the queryset if the user is an admin now includes all surveys,
            therefore when the list api is requested, just returns that users surveys
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        qs = RentingSurveyModel.objects.filter(user_profile=user_profile)
        serializer = RentSurveySerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a survey based on either the id or the survey url
        :param request:
        :param args:
        :param kwargs:
            type: 'by_url' -> The survey is retrieved by using the survey url
                   other -> Anything else will default the request to retrieve the survey via id
            data_type: 'survey_subscribe' -> Returns the data just for the survey subscribe data
                        other -> Returns the Survey Serialized data
            pk: Stores either the survey url or the survey depending on the type
        :return: A serialized response with the survey that was retrieved
        """
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Determine the method for getting the survey
        retrieve_type = self.request.query_params.get('type', None)
        data_type = self.request.query_params.get('data_type', None)

        # Retrieve the survey id/url
        pk = kwargs.pop('pk', None)

        if retrieve_type == 'by_url':
            # Retrieve the associated survey with the request
            survey = retrieve_survey(user_profile, url=pk)
        else:
            survey = retrieve_survey(user_profile, pk=pk)

        if data_type == 'survey_subscribe':
            serializer = SurveySubscribeSerializer(survey)
            return Response(serializer.data)
        else:
            serializer = RentSurveySerializer(survey, context={'user': user_profile.user})
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Retrieves all the data from the frontend
        Then the data is parsed to each of the sections
        If all the forms are valid, they are saved and the redirect url is returned
        Otherwise the form errors are returned
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = self.request.data['data']

        # Parse data to correct format
        survey_data = None
        tenant_data = None
        user_data = None

        # Save data if it exists
        if 'generalInfo' in data:
            survey_data = data['generalInfo']
        if 'amenitiesInfo' in data:
            survey_data.update(data['amenitiesInfo'])
        if 'tenantInfo' in data:
            tenant_data = data['tenantInfo']
        if 'detailsInfo' in data:
            user_data = data['detailsInfo']

        form = RentSurveyForm(survey_data)
        tenants = TenantFormSet(tenant_data)
        user_form = None

        user = self.request.user
        if user.is_anonymous():
            user = None
        user_signing_in = False

        # Determines if the user is trying to sign in or create a new account and creates
        #   the corresponding form
        if not self.request.user.is_authenticated():
            if user_data.get('user_logging_in', False):
                user_signing_in = True
                user_form_data = {
                    'username': user_data.get('email'),
                    'password': user_data.get('password1'),
                }
                user_form = LoginUserForm(request, user_form_data)
            else:
                user_form = ApartmentHunterSignupForm(user_data)

        # Determines if any of the forms is not valid, and only check user_form if it exists
        forms_valid = form.is_valid() and tenants.is_valid() and user_form.is_valid() if user_form is not None else True

        # Only bother checking if all the forms are valid and there is a user_form
        # Called after checking to see if all the forms are valid
        if forms_valid and user_form is not None:
            # If the user is trying to login then authenticate them, otherwise try to create a new user
            if user_signing_in:
                user = authenticate(username=user_form.cleaned_data.get('username'),
                                    password=user_form.cleaned_data.get('password'))
                if user is not None:
                    login(request, user)
            else:
                user = user_form.save(request=self.request)
                login(self.request, user)

        # If the forms are valid and the user is successfully, logged in either via creating, signing up or already
        #   been logged in, then start the process of saving the survey
        if forms_valid and user is not None:

            # Save the form information
            with transaction.atomic():

                # Save the rent survey
                form.instance.user_profile = get_object_or_404(UserProfile, user=user)

                # Now the form can be saved
                survey = form.save()
                survey.url = survey.generate_slug()
                if 'num_bedrooms' in survey_data:
                    survey.num_bedrooms = survey_data['num_bedrooms']
                survey.save()

                # Save the polygons
                if 'polygons' in survey_data and 'polygon_filter_type' in survey_data:
                    save_polygons(survey, survey_data['polygons'], survey_data['polygon_filter_type'])

                # Now save the the tenants
                tenants.instance = survey
                tenants.save()

            survey = RentingSurveyModel.objects.get(id=survey.id)

            # Return that the result is True and the redirect url so the page knows
            #   where to redirect to
            return Response({'result': True, 'redirect_url': survey.url})

        else:

            # If there were any errors then save the errors so they can be returned
            form_errors = form.errors
            user_form_errors = ""
            tenants_errors = ""
            sign_failure = ""

            if tenants is not None:
                tenants.is_valid()
                tenants_errors = tenants.errors

            if user_form is not None:
                user_form.is_valid()
                user_form_errors = user_form.errors
                if user is None and user_data.get('user_logging_in', False):
                    user_form_errors['sign_in_failure'] = "Login failed, please retry your credentials"
                logger.error("In Survey creation:\n"
                             "User: {0} {1}.\n"
                             "Had errors form errors:{2}\n"
                             "tenant_erorrs: {3}\n"
                             "user_form errors: {4}\n".format(user_form.data.get('first_name'),
                                                              user_form.data.get('last_name'),
                                                              form_errors,
                                                              tenants_errors,
                                                              user_form_errors))
            else:
                logger.error("In Survey Creation:\n"
                             "User: {0} \n"
                             "Had errors form errors:{1}\n"
                             "tenant_erorrs: {2}\n"
                             "user_form errors: {3}\n".format(self.request.user.full_name,
                                                              form_errors,
                                                              tenants_errors,
                                                              user_form_errors))

            # Return a result false if the form was not valid
            return Response({
                'result': False,
                'survey_errors': form_errors,
                'tenants_errors': tenants_errors,
                'user_form_errors': user_form_errors
            })

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
                        survey_edit: Updates a survey with new data
                        survey_subscribe: Update the survey subscribe data
                data: (json) -> The data associated with the request
        :return:
            Dependent on type:
                survey_edit:
                {
                    result: (Boolean) -> True: The operation succeeded
                                         False: The operation failed
                        if True:
                            survey: (RentSurveyModel) -> The updated survey
                        if False:
                            survey_errors: Errors associated with the survey
                            tenants_errors: Errors assocaited with the tenant

                }
        """

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

        # Retrieve the associated survey with the request
        survey = retrieve_survey(user_profile, pk=pk)

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

        elif 'survey_edit' in self.request.data['type']:
            data = self.request.data['data']

            # Parse data to correct format
            survey_data = None
            tenant_data = None

            # Save data if it exists
            if 'generalInfo' in data:
                survey_data = data['generalInfo']
            if 'amenitiesInfo' in data:
                survey_data.update(data['amenitiesInfo'])
            if 'tenantInfo' in data:
                tenant_data = data['tenantInfo']

            form = RentSurveyFormEdit(survey_data, instance=survey)
            tenants = None

            if form.is_valid():
                tenants = TenantFormSet(tenant_data, instance=survey)
                if tenants.is_valid():

                    with transaction.atomic():
                        if 'num_bedrooms' in survey_data:
                            survey.num_bedrooms = survey_data['num_bedrooms']
                        survey = form.save()

                        # Save the polygons
                        if 'polygons' in survey_data and 'polygon_filter_type' in survey_data:
                            save_polygons(survey, survey_data['polygons'], survey_data['polygon_filter_type'])

                        # Now save the the tenants
                        tenants.save()

                    serializer = RentSurveySerializer(survey, context={'user': user_profile.user})
                    return Response({'result': True, 'survey': serializer.data})

            tenants_errors = ""
            if tenants is not None:
                tenants.is_valid()
                tenants_errors = tenants.errors

            logger.error("In Survey edit:\n"
                         "User: {0} \n"
                         "Had errors form errors:{1}\n"
                         "tenant_erorrs: {2}\n".format(self.request.user.full_name,
                                                       form.errors,
                                                       tenants_errors))

            return Response({
                'result': False,
                'survey_errors': form.errors,
                'tenants_errors': tenants_errors,
            })
        elif 'survey_subscribe' in self.request.data['type']:
            data = self.request.data['data']

            # Update the information with regards to the survey subscribe
            with transaction.atomic():
                try:
                    if not data['num_home_threshold'] == "":
                        survey.num_home_threshold = data['num_home_threshold']
                    if not data['wants_update'] == "":
                        survey.wants_update = data['wants_update']
                    if not data['score_threshold'] == "":
                        survey.score_threshold = data['score_threshold']
                    survey.save()
                except ValueError:
                    pass

            # Return the new data saved by the survey
            serializer = SurveySubscribeSerializer(survey)
            return Response(serializer.data)

        # Returns the survey that was updated
        serializer = RentSurveySerializer(survey, context={'user': user_profile.user})
        return Response(serializer.data)


class RentResultViewSet(viewsets.ViewSet):
    """
    This view set runs the survey algorithm. Given a survey that the user has
        it computes the best homes
    """

    def retrieve(self, request, pk=None):
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey
        survey = retrieve_survey(user_profile, url=pk)

        # Run the Rent Algorithm
        rent_algorithm = RentAlgorithm()
        rent_algorithm.run(survey)

        # Asynchronously compute the survey results iteration
        home_scores = [x.percent_score() for x in rent_algorithm.homes]
        compute_survey_result_iteration_task.delay(survey.id, user_profile.id, home_scores)

        # Save the response
        data = [x for x in rent_algorithm.homes[:NUMBER_OF_HOMES_RETURNED] if x.percent_score() >= 0]

        # Blacklist homes that show up to the user
        for home_score in rent_algorithm.homes[:NUMBER_OF_HOMES_RETURNED]:
            survey.blacklist_home(home_score.home)

        # Serialize the response
        serializer = HomeScoreSerializer(data, many=True, context={'user': user_profile.user})

        # Return the result
        return Response(serializer.data)


class TenantViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    def update(self, request, *args, **kwargs):
        """
        This updates the tenants name for a given survey
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

        # Retrieve the associated survey with the request
        survey = retrieve_survey(user_profile, pk=pk)

        tenant_data = self.request.data['data']

        tenants = TenantFormSetJustNames(tenant_data, instance=survey)

        # Test if form is valid
        if tenants.is_valid():

            # Save tenants form
            tenants.save()

        # Retrieve the associated survey with the request
        survey = retrieve_survey(user_profile, pk=pk)
        serializer = RentSurveySerializer(survey, context={'user': user_profile.user})
        return Response(serializer.data)


def retrieve_survey_queryset(user_profile):
    """
    Retrieves the correct queryset for the survey. If the user is an admin then any survey can
        be retrieved. Otherwise the user is limited to their own surveys.
    :param user_profile: (UserProfile Model) -> The user associated with the request
    :return: (RentingSurveyModel Queryset) -> The queryset that the user is allowed to choose from
    """
    if user_profile.user.is_admin:
        return RentingSurveyModel.objects.all()
    else:
        return RentingSurveyModel.objects.filter(user_profile=user_profile)


def retrieve_survey(user_profile, url=None, pk=None):
    """
    Retrieves a survey depending on the arguments that are given. If the pk is given it used that by
        default. If not then if the url is given then it will try to get the survey based off of that.
        If neither is given then a 404 is returned
    :param user_profile: (UserProfile Model) -> The user associated with the request
    :param url: (string) -> The user of the survey
    :param pk: (int) -> The id of the survey
    :return: The survey or a 404
    """
    if pk is not None:
        if user_profile.user.is_admin:
            return get_object_or_404(RentingSurveyModel, id=pk)
        else:
            return get_object_or_404(RentingSurveyModel, user_profile=user_profile, id=pk)
    elif url is not None:
        if user_profile.user.is_admin:
            return get_object_or_404(RentingSurveyModel, url=url)
        else:
            return get_object_or_404(RentingSurveyModel, user_profile=user_profile, url=url)
    else:
        raise Http404



