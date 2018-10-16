# load django modules
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Load Cocoon Modules
from cocoon.signature.models import HunterDocManagerModel, HunterDocTemplateModel
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

    return render(request, 'signature/signature_page.html', context)
