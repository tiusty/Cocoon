# Import Django Modules
from django.test import TestCase

# Import Cocoon modules
from cocoon.signature.models import HunterDocModel, HunterDocTemplateModel, HunterDocManagerModel
from cocoon.userAuth.models import MyUser
from cocoon.signature.docusign.docusign_wrapper import DocusignWrapper
from cocoon.signature.docusign.docusign_base import DocusignLogin

# Import third party modules
from unittest.mock import MagicMock

# Import Constants
from cocoon.signature.constants import PRE_TOUR_TEMPLATE_ID


class TestSignatureModelsAllDocuments(TestCase):

    def test_is_all_signed_no_documents(self):
        """
        Tests that if there are no documents in the template model then is_all_signed returns True
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)

        # Act/Assert
        self.assertTrue(manager.is_all_documents_signed())

    def test_is_all_signed_no_documents_one_template(self):
        """
        Tests that if there is one document template and no documents then is_all_signed is false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id="123")

        # Act/Assert
        self.assertFalse(manager.is_all_documents_signed())

    def test_is_all_signed_one_document_signed(self):
        """
        Tests that if there is one document and one template and the documents is signed,
            then the is_all_signed returns true
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id="123")

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=True)

        # Assert
        self.assertTrue(manager.is_all_documents_signed())

    def test_is_all_signed_one_document_not_signed(self):
        """
        Tests that if one document exists and one template and the document is not signed,
            then return false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id="123")

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=False)

        # Assert
        self.assertFalse(manager.is_all_documents_signed())

    def test_is_all_signed_two_documents_signed(self):
        """
        Tests that if there is two documents and two templates and the documents are both signed,
        then the is_all_signed returns true
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id="123")
        template2 = HunterDocTemplateModel.objects.create(template_type="tb", template_id="123")

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=True)
        manager.documents.create(template=template2, envelope_id="122", is_signed=True)

        # Assert
        self.assertTrue(manager.is_all_documents_signed())

    def test_is_all_signed_one_document_signed_one_not(self):
        """
        Tests that if there are two templates and two documents and one of the documents is not signed,
            then is_all_signed returns false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id="123")
        template2 = HunterDocTemplateModel.objects.create(template_type="tb", template_id="123")

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=True)
        manager.documents.create(template=template2, envelope_id="122", is_signed=False)

        # Assert
        self.assertFalse(manager.is_all_documents_signed())


class TestSignatureModelsPreTourDocuments(TestCase):

    def test_is_pre_tour_signed_without_creating_template(self):
        """
        Tests that if the is_pre_tour_singed is called without creating the pre_tour template,
            then the function returns false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)

        # Assert
        self.assertFalse(manager.is_pre_tour_signed())

    def test_is_pre_tour_signed_without_creating_document(self):
        """
        Tests that if the pre_tour template is created but if no documents are created,
            then the function returns false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id=PRE_TOUR_TEMPLATE_ID)

        # Assert
        self.assertFalse(manager.is_pre_tour_signed())

    def test_is_pre_tour_signed_true(self):
        """
        Tests that if there is a document that is signed and is apart of the pre_tour template
            then the is_pre_tour_signed returns true
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id=PRE_TOUR_TEMPLATE_ID)

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=True)

        # Assert
        self.assertTrue(manager.is_pre_tour_signed())

    def test_is_pre_tour_signed_false(self):
        """
        Tests that if the template and document for pre_tour is created but the document
            is not signed, then the function returns false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id=PRE_TOUR_TEMPLATE_ID)

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=False)

        # Assert
        self.assertFalse(manager.is_pre_tour_signed())

    def test_is_pre_tour_signed_wrong_template(self):
        """
        Tests that if there is a document which is signed but it not the pre_tour document,
            then the pre_tour_singed returns false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.objects.create(template_id="123", template_type="np")

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=True)

        # Assert
        self.assertFalse(manager.is_pre_tour_signed())

    def test_create_pre_tour_documents_send(self):
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com", first_name="TestName", last_name="TestLast")
        manager = HunterDocManagerModel.objects.create(user=user)
        HunterDocTemplateModel.create_pre_tour_template()
        DocusignLogin.set_up_docusign_api = MagicMock()
        DocusignWrapper.send_document_for_signatures = MagicMock(return_value="123")

        # Act
        result = manager.create_pre_tour_documents()

        # Assert
        self.assertTrue(result)
        self.assertEqual(HunterDocModel.objects.count(), 1)
        self.assertEqual(HunterDocModel.objects.first().template,
                         HunterDocTemplateModel.objects.get(template_type=HunterDocTemplateModel.PRE_TOUR))

    def test_create_pre_tour_documents_template_does_not_exist(self):
        """
        Since the template is created when it is accessed, this should pass and return true
        :return:
        """
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com", first_name="TestName", last_name="TestLast")
        manager = HunterDocManagerModel.objects.create(user=user)
        DocusignLogin.set_up_docusign_api = MagicMock()
        DocusignWrapper.send_document_for_signatures = MagicMock(return_value="123")

        # Act
        result = manager.create_pre_tour_documents()

        # Assert
        self.assertTrue(result)

