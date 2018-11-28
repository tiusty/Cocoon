# load django modules
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

# Rest Framework
from rest_framework import viewsets
from rest_framework.response import Response

# Load app modules
from .models import HunterDocManagerModel, HunterDocTemplateModel, HunterDocModel
from .serializers import HunterDocManagerSerializer, HunterDocSerializer, HunterDocTemplateSerializer

# Load Cocoon Modules
from cocoon.userAuth.models import UserProfile


@login_required
def signature_page(request):
    context = {
        'error_message': []
    }

    # Retrieve the models
    user_profile = get_object_or_404(UserProfile, user=request.user)
    (manager, _) = HunterDocManagerModel.objects.get_or_create(
        user=user_profile.user,
    )

    # Update all the documents status before loading
    manager.update_all_is_signed()

    # Retrieve all the template types
    template_types = HunterDocTemplateModel.objects.all()
    docs = []

    # Either stores the corresponding document with a True or
    #   stores False and then the template type that is missing
    for template in template_types:
        if manager.documents.filter(template=template).exists():
            docs.append((True, manager.documents.filter(template=template).first()))
        else:
            docs.append((False, template))

    context['template_types'] = docs
    context['user'] = user_profile.user
    context['component'] = 'SignaturePage'

    return render(request, 'signature/signature_page.html', context)

#############################################
# Api views below
#############################################


class HunterDocTemplateViewset(viewsets.ModelViewSet):

    queryset = HunterDocTemplateModel.objects.all()
    serializer_class = HunterDocTemplateSerializer


@method_decorator(login_required, name='dispatch')
class HunterDocViewset(viewsets.ModelViewSet):

    serializer_class = HunterDocSerializer

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return user_profile.user.doc_manager.documents

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a Doc by the pk of the HunterDocTemplate
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

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
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        template_id = self.request.data['template_type_id']

        template = get_object_or_404(HunterDocTemplateModel, id=template_id)

        if template.template_type == HunterDocTemplateModel.PRE_TOUR:
            user_profile.user.doc_manager.create_pre_tour_documents()
        else:
            raise Http404

        doc = HunterDocModel.objects.get(doc_manager=user_profile.user.doc_manager, template=template)
        serializer = HunterDocSerializer(doc)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

        template = get_object_or_404(HunterDocTemplateModel, pk=pk)

        if template.template_type == HunterDocTemplateModel.PRE_TOUR:
            user_profile.user.doc_manager.update_pre_tour_is_signed()

        doc = HunterDocModel.objects.get(doc_manager=user_profile.user.doc_manager, template=template)
        serializer = HunterDocSerializer(doc)
        return Response(serializer.data)




@method_decorator(login_required, name='dispatch')
class HunterDocManagerViewset(viewsets.ModelViewSet):

    serializer_class = HunterDocManagerSerializer

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return HunterDocManagerModel.objects.filter(user=user_profile.user)

    def update(self, request, *args, **kwargs):
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
