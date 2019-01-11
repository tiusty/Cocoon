# load django modules
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.views.generic import TemplateView

# Rest Framework
from rest_framework import viewsets
from rest_framework.response import Response

# Load app modules
from .models import HunterDocManagerModel, HunterDocTemplateModel, HunterDocModel
from .serializers import HunterDocManagerSerializer, HunterDocSerializer, HunterDocTemplateSerializer

# Load Cocoon Modules
from cocoon.userAuth.models import UserProfile


@method_decorator(login_required, name='dispatch')
class SignaturePage(TemplateView):

    template_name = 'signature/signature_page.html'

    def get_context_data(self, **kwargs):
        """
        Adds the TenantFormSet, and the user creation form to the context
        """
        data = super().get_context_data(**kwargs)
        data['component'] = 'SignaturePage'
        return data


#############################################
# Api views below
#############################################


class HunterDocTemplateViewset(viewsets.ReadOnlyModelViewSet):
    """
    Returns all the HunterDocTemplates
    """

    queryset = HunterDocTemplateModel.objects.all()
    serializer_class = HunterDocTemplateSerializer


class HunterDocViewset(viewsets.ModelViewSet):

    serializer_class = HunterDocSerializer

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return user_profile.user.doc_manager.documents

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a Doc by the pk of the HunterDocTemplate. The pk is passed via the url

        i.e

        hunterDoc/1/ -> Returns a document for that user that is associated with hunter doc template 1

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

        # To easily pass back whether the document has been created or not return a Json response
        #   of a result variable which is true when the document is already created or false otherwise,
        #   and then pass the serializer as another field. The serializer will be blank if the document
        #   is not created, i.e result = false.
        try:
            doc = HunterDocModel.objects.get(doc_manager=user_profile.user.doc_manager, template=pk)
            response = {
                'result': True,
                'serializer': HunterDocSerializer(doc).data,
            }
        except HunterDocModel.DoesNotExist:
            response = {
                'result': False,
                'serializer': '',
            }

        return Response(response)

    def create(self, request, *args, **kwargs):
        """
        API to create a new document.

        Expects a template_type_id to be passed in which determines which type of document is created

        :param request:
        :param args:
        :param kwargs:
            Expects:
                template_type_id: (string) -> The template type id associated with the document
        :return:
        """

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        template = None

        if 'template_type_id' in self.request.data:
            template_id = self.request.data['template_type_id']

            template = get_object_or_404(HunterDocTemplateModel, id=template_id)

            # Determine the template type used and update that document
            if template.template_type == HunterDocTemplateModel.PRE_TOUR:
                user_profile.user.doc_manager.create_pre_tour_documents()
            else:
                # If the template type does not match any of the necessary template types then
                #   return 404
                raise Http404

        # Case if the request has type in the data
        elif 'type' in self.request.data:
            doc_type = self.request.data['type']
            if doc_type == 'pre_tour':
                user_profile.user.doc_manager.create_pre_tour_documents()
                template = user_profile.user.doc_manager.retrieve_pre_tour_template()
            else:
                raise Http404

        doc = HunterDocModel.objects.get(doc_manager=user_profile.user.doc_manager, template=template)
        serializer = HunterDocSerializer(doc)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        API to update a documents status via the template type

        The document itself is not passed in, instead the id for the template type is passed in
            and depending on the template type the corresponding update function for that users
            doc manager is called

        :param request:
        :param args:
        :param kwargs:
            Expects:
                pk: (int) -> The value passed in via the url
                type: (string) -> The type of update specified
                    One of:
                        update -> Update the document with the passed in template id
                        resend -> Resend the document with the passed in template id
        :return:
        """
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

        template = get_object_or_404(HunterDocTemplateModel, pk=pk)

        # Update, updates the status of the document with the given template id
        if 'update' in self.request.data['type']:
            if template.template_type == HunterDocTemplateModel.PRE_TOUR:
                user_profile.user.doc_manager.update_pre_tour_is_signed()
        # resend, resends the document to the user via email
        elif 'resend' in self.request.data['type']:
            if template.template_type == HunterDocTemplateModel.PRE_TOUR:
                user_profile.user.doc_manager.resend_pre_tour_documents()

        # Return the document again
        doc = HunterDocModel.objects.get(doc_manager=user_profile.user.doc_manager, template=template)
        serializer = HunterDocSerializer(doc)
        return Response(serializer.data)


class HunterDocManagerViewset(viewsets.ModelViewSet):
    """
    Returns the Hunter Document Manager
    """

    serializer_class = HunterDocManagerSerializer

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return HunterDocManagerModel.objects.filter(user=user_profile.user)

    def update(self, request, *args, **kwargs):
        """
        Updates a document via a variable determines which template type to update

        :param request:
        :param args:
        :param kwargs:
            Expects:
                type: (string) -> The update type that is occurring
                    One of:
                        pre_tour_check: Updates the pre tour document status
        :return:
        """
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the associated survey with the request
        doc_manager = user_profile.user.doc_manager

        # If the request wants to check pre_tour docs then check the pre_tour docs and see if it is signed
        if 'pre_tour_check' in self.request.data['type']:
            doc_manager.update_pre_tour_is_signed()

        # Retrieve the doc_manager again with updated values
        doc_manager = user_profile.user.doc_manager
        serializer = HunterDocManagerSerializer(doc_manager)
        return Response(serializer.data)
