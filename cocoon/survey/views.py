# Import Django modules
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import login
from django.views.generic import TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Import House Database modules
from cocoon.houseDatabase.models import RentDatabaseModel

# Import User Auth modules
from cocoon.userAuth.models import UserProfile

# Import Survey algorithm modules
from .cocoon_algorithm.rent_algorithm import RentAlgorithm
from .models import RentingSurveyModel
from .forms import RentSurveyForm, TenantFormSet, TenantFormSetJustNames
from .survey_helpers.save_polygons import save_polygons
from .serializers import HomeScoreSerializer, RentSurveySerializer

# Cocoon Modules
from cocoon.userAuth.forms import ApartmentHunterSignupForm

# Rest Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


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
        return RentingSurveyModel.objects.filter(user_profile=user_profile)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['component'] = RentingResultTemplate.__name__
        return data


class RentSurveyViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                        mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = RentSurveySerializer

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
        return RentingSurveyModel.objects.filter(user_profile=user_profile)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a survey based on either the id or the survey url
        :param request:
        :param args:
        :param kwargs:
            type: 'by_url' -> The survey is retrieved by using the survey url
                   other -> Anything else will default the request to retrieve the survey via id
            pk: Stores either the survey url or the survey depending on the type
        :return: A serailzed response with the survey that was retrieved
        """
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Determine the method for getting the survey
        retrieve_type = self.request.query_params.get('type', None)

        # Retrieve the survey id/url
        pk = kwargs.pop('pk', None)

        if retrieve_type == 'by_url':
            # Retrieve the associated survey with the request
            survey = get_object_or_404(RentingSurveyModel, user_profile=user_profile, url=pk)
        else:
            survey = get_object_or_404(RentingSurveyModel, user_profile=user_profile, id=pk)

        serializer = RentSurveySerializer(survey)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Retrieves all the data from the frontend
        Then the data is parsed to each of the sections
        If all the forms are valid, they are saved and the redirct url is returned
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

        number_of_tenants = survey_data['number_of_tenants']
        form = RentSurveyForm(survey_data)

        tenants = None
        user_form = None

        if form.is_valid():

            tenants = TenantFormSet(tenant_data)

            does_user_signup = False
            sign_up_form_valid = True

            if not self.request.user.is_authenticated():
                does_user_signup = True
                user_form = ApartmentHunterSignupForm(user_data)
                sign_up_form_valid = user_form.is_valid()

            # Makes sure that the tenant form and the signup form are valid before saving
            if tenants.is_valid() and sign_up_form_valid:

                user = self.request.user

                # If the user is signing up then save that form and return the user to log them in
                if does_user_signup:
                    user = user_form.save(request=self.request)
                    login(self.request, user)

                # Save the rent survey
                with transaction.atomic():
                    form.instance.user_profile = get_object_or_404(UserProfile, user=user)

                    # Now the form can be saved
                    survey = form.save()
                    survey.url = survey.generate_slug()
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

        # If there were any errors then save the errors so they can be returned
        form_errors = form.errors
        user_form_errors = ""
        tenants_errors = ""

        if tenants is not None:
            tenants.is_valid()
            tenants_errors = tenants.errors

        if user_form is not None:
            user_form.is_valid()
            user_form_errors = user_form.errors

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

            form = RentSurveyForm(survey_data, instance=survey)
            tenants = None

            if form.is_valid():
                tenants = TenantFormSet(tenant_data, instance=survey)
                if tenants.is_valid():

                    with transaction.atomic():
                        survey = form.save()

                        # Save the polygons
                        if 'polygons' in survey_data and 'polygon_filter_type' in survey_data:
                            save_polygons(survey, survey_data['polygons'], survey_data['polygon_filter_type'])

                        # Now save the the tenants
                        tenants.save()

                    serializer = RentSurveySerializer(survey)
                    return Response({'result': True, 'survey': serializer.data})

            tenants_errors = ""
            if tenants is not None:
                tenants.is_valid()
                tenants_errors = tenants.errors

            return Response({
                'result': False,
                'survey_errors': form.errors,
                'tenants_errors': tenants_errors,
            })

        # Returns the survey that was updated
        serializer = RentSurveySerializer(survey)
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
        survey = get_object_or_404(RentingSurveyModel, user_profile=user_profile, url=pk)

        # Run the Rent Algorithm
        rent_algorithm = RentAlgorithm()
        rent_algorithm.run(survey)

        # Save the response
        data = [x for x in rent_algorithm.homes[:25] if x.percent_score() >= 0]

        # Serialize the response
        serializer = HomeScoreSerializer(data, many=True)

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
        survey = get_object_or_404(RentingSurveyModel, user_profile=user_profile, pk=pk)

        tenant_data = self.request.data['data']

        tenants = TenantFormSetJustNames(tenant_data, instance=survey)

        # Test if form is valid
        if tenants.is_valid():

            # Save tenants form
            tenants.save()

        # Retrieve the associated survey with the request
        survey = get_object_or_404(RentingSurveyModel, user_profile=user_profile, pk=pk)
        serializer = RentSurveySerializer(survey)
        return Response(serializer.data)
