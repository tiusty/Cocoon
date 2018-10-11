from django.db import models
from django.shortcuts import get_object_or_404

# Cocoon modules
from cocoon.userAuth.models import MyUser

# Load the logger
import logging
logger = logging.getLogger(__name__)


class HunterDocManagerModel(models.Model):
    user = models.OneToOneField(MyUser, related_name="doc_manager", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name

    def is_all_documents_signed(self):
        # If the number of documents is less than the number of template documents
        #   then automatically there are unsigned documents
        if HunterDocTemplateModel.objects.count() > self.documents.count():
            return False

        # For all the documents check to see if there are any that are not unsigned
        for document in self.documents.all():
            if not document.is_signed:
                return False
        return True

    def is_pre_tour_signed(self):
        try:
            template = HunterDocTemplateModel.objects.get(template_type=HunterDocTemplateModel.PRE_TOUR)
        except HunterDocTemplateModel.DoesNotExist:
            logger.warning("Tried to retrieve the pre_tour_template but it did not exist")
            return False

        if self.documents.filter(template=template).exists():
            doc = get_object_or_404(HunterDocModel, template=template)
            return doc.is_signed
        else:
            logger.warning("is_pre_tour_signed else statement reached")
            return False


class HunterDocTemplateModel(models.Model):
    """
        Atributes:
            self.template_type (string) -> What the template corresponds to, i.e pre_tour forms, renting forms etc
            self.tempalte_id (string) -> The template id from docusign that corresponds to the type of template
    """
    PRE_TOUR = 'pt'
    DOC_TYPE = (
        (PRE_TOUR, 'Pretour forms'),
    )

    template_type = models.CharField(
        unique=True,
        max_length=2,
        choices=DOC_TYPE,
        default=PRE_TOUR,
    )
    template_id = models.CharField(max_length=200)

    def __str__(self):
        return self.get_template_type_display()


class HunterDocModel(models.Model):
    doc_manager = models.ForeignKey(HunterDocManagerModel, related_name="documents", on_delete=models.CASCADE)
    template = models.ForeignKey(HunterDocTemplateModel, related_name="templates", on_delete=models.CASCADE)
    is_signed = models.BooleanField(default=False)
    envelope_id = models.CharField(max_length=200)

    def __str__(self):
        return "{0} Document".format(self.template.get_template_type_display())
