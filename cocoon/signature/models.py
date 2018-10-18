from django.db import models
from django.shortcuts import get_object_or_404

# Import docusign wrapper classes
from cocoon.signature.docusign.docusign_wrapper import DocusignWrapper

# Cocoon modules
from cocoon.userAuth.models import MyUser

# Import constants
from cocoon.signature.constants import PRE_TOUR_TEMPLATE_ID

# Load the logger
import logging
logger = logging.getLogger(__name__)


class HunterDocManagerModel(models.Model):
    """
    Each Hunter has a corresponding Document manager. This stores all the documents that are linked to a
        particular user

    Attributes:
        self.user: (OneToOneField) -> A link to the user that the doc manager is related to
    """
    user = models.OneToOneField(MyUser, related_name="doc_manager", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name

    def is_all_documents_signed(self):
        """
        Returns where or not all the documents for the given doc manager is signed.
            Each user only has one doc manager so this also determines whether or not
            the user signed all their paper work
        :return: (Boolean) -> True: The user signed all the documents
                              False: The user has not signed all the documents
        """
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
        if self.documents.filter(template=template).exists():
            try:
                doc = get_object_or_404(HunterDocModel, template=template, doc_manager=self)
                return doc.is_signed
            except HunterDocModel.DoesNotExist:
                return False
        else:
            return False

    def create_pre_tour_documents(self):
        """
        Creates the pre_tour document. This will create the object in the database as well as send a request to docusign
        If the request is successfully sent and the envelope_id is generated, then the object in the database is created.
        Otherwise the object is not created in the database

        :return: (boolean) -> True: The document was successfully created
                              False: The document was not successfully created
        """
        template = self.retrieve_pre_tour_template()
        docusign = DocusignWrapper()
        envelope_id = docusign.send_document_for_signatures(template.template_id,
                                                            self.user.email,
                                                            self.user.full_name)
        if envelope_id is not None:
            self.documents.create(envelope_id=envelope_id, template=template)
            return True

        return False

    def pre_tour_forms_created(self):
        """
        Returns whether or not the pre_tours forms are created. This does not
            say anything about whether or not the forms were signed
        :return: (boolean) -> True: The pre_tour forms were created
                              False: The pre_tour forms were not created
        """
        template = self.retrieve_pre_tour_template()
        return self.documents.filter(template=template).exists()

    def resend_pre_tour_documents(self):
        """
        Re-sends the pre tour forms to the user.
        This is used in case they lost it etc and need it resent to their email
        :return: (boolean) -> True: If the pre tour documents are resent
                              False: IF the pre tour documents are not resent
        """
        template = self.retrieve_pre_tour_template()
        docusign = DocusignWrapper()
        if self.documents.filter(template=template).exists():
            try:
                document = self.documents.get(template=template)
                envelope_id = document.envelope_id
            except HunterDocModel.DoesNotExist:
                logger.error("Tried to return Document that does not exist: {0}".format(
                    HunterDocManagerModel.resend_pre_tour_documents.__name__
                ))
                return False
            except HunterDocModel.MultipleObjectsReturned:
                logger.error("Multiple objects returned in: {0}".format(
                    HunterDocManagerModel.resend_pre_tour_documents.__name__
                ))
                return False
            return docusign.resend_envelope(envelope_id)
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
            document.save()

    @staticmethod
    def retrieve_pre_tour_template():
        """
        Wrapper class to retrieve the pre_tour template

        This will either return the template if it exists, or creates it with the correct
            template_id if it doesn't exist
        :return: (HunterDocTemplateModel) -> Returns the pre tour template model
        """
        (template, created) = HunterDocTemplateModel.objects.get_or_create(
            template_type=HunterDocTemplateModel.PRE_TOUR,
            template_id=PRE_TOUR_TEMPLATE_ID,
        )
        return template


class HunterDocTemplateModel(models.Model):
    """
        This stores the template id for the document. This is where the forms were generated from
        Attributes:
            self.template_type (string) -> What the template corresponds to, i.e pre_tour forms, renting forms etc
            self.tempalte_id (string) -> The template id from docusign that corresponds to the type of template
    """
    PRE_TOUR = 'pt'
    DOC_TYPE = (
        (PRE_TOUR, 'Pre-tour forms'),
    )

    template_type = models.CharField(
        unique=True,
        max_length=2,
        choices=DOC_TYPE,
        default=PRE_TOUR,
    )
    template_id = models.CharField(max_length=200)

    @staticmethod
    def create_pre_tour_template():
        """
        Creates the pre_tour_template with the correct template_id
        :return: (HunterDocTemplateModel) -> The created template
        """
        (template, created) = HunterDocTemplateModel.objects.get_or_create(
            template_type=HunterDocTemplateModel.PRE_TOUR,
            template_id=PRE_TOUR_TEMPLATE_ID,
        )
        return template

    def __str__(self):
        return self.get_template_type_display()


class HunterDocModel(models.Model):
    """
    This stores information specific to a document. This stores what the template for the document is, which user
        it is associated with, what the enevelope ID to find it on Docusign and whether or not the document is signed

    Attributes:
        self.doc_manager: (ForeignKey(HunterDocManager)) -> The associated doc manager that the document is linked to
        self.template: (ForeignKey(HunterDocTemplateModel)) -> The template that is associated with the document
        self.is_signed: (Boolean) -> Whether or not the document is signed
        self.envelope_id: (string) -> The envelope id corresponding to the document on docusign
    """
    doc_manager = models.ForeignKey(HunterDocManagerModel, related_name="documents", on_delete=models.CASCADE)
    template = models.ForeignKey(HunterDocTemplateModel, related_name="documents", on_delete=models.CASCADE)
    is_signed = models.BooleanField(default=False)
    envelope_id = models.CharField(max_length=200)

    def __str__(self):
        return "{0} Document".format(self.template.get_template_type_display())
