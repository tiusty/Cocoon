from django.db import models
from django.shortcuts import get_object_or_404

# Import docusign wrapper classes
from cocoon.signature.docusign.docusign_list_documents import DocusignWrapper

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
        """
        Determines if the pre_tour document is signed.
        :return: (boolean) -> True: The document is signed
                              False: The document is not signed
        """
        template = self.retrieve_pre_tour_template()
        if template is not None:
            if self.documents.filter(template=template).exists():
                try:
                    doc = get_object_or_404(HunterDocModel, template=template)
                    return doc.is_signed
                except HunterDocModel.DoesNotExist:
                    return False
            else:
                return False
        else:
            return False

    def create_pre_tour_documents(self):
        """
        Creates the pre_tour document. This will create the object in the database as well as send a request to docusign
        If the request is successfully sent and the envelope_id is generated, then the object in the database is created.
        Otherwise the object is not created in the database
        """
        template = self.retrieve_pre_tour_template()
        if template is not None:
                docusign = DocusignWrapper()
                envelope_id = docusign.send_document_for_signatures("e998b44f-28cb-4d20-ad67-97a033cbbab1",
                                                                    self.user.email,
                                                                    self.user.full_name)
                if envelope_id is not None:
                    self.documents.create(envelope_id=envelope_id, template=template)
                    return True

                return False
        else:
            return False

    def update_all_is_signed(self):
        """
        Retrieves all the documents that the user has and checks in docusign for the status of the document
            If the status is complete then the document is signed, otherwise it is not signed
        """
        docusign = DocusignWrapper()
        for document in self.documents.all():
            document.is_signed = docusign.determine_is_signed(document.envelope_id)

    @staticmethod
    def retrieve_pre_tour_template():
        try:
            return HunterDocTemplateModel.objects.get(template_type=HunterDocTemplateModel.PRE_TOUR)
        except HunterDocTemplateModel.DoesNotExist:
            logger.error("Tried to retrieve the pre_tour_template but it did not exist")
            return None


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
