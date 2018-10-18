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
        HunterDocTemplateModel.objects.create(template_id="123")

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

    def test_is_all_signed_multiple_users(self):
        """
        Tests that if there are multiple users, the users documents don't conflict. I.e the user with all
            the documents signed returns true and the other returns false
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        user1 = MyUser.objects.create(email="test@test1.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        manager1 = HunterDocManagerModel.objects.create(user=user1)
        template = HunterDocManagerModel.retrieve_pre_tour_template()
        template2 = HunterDocTemplateModel.objects.create(template_type="tb", template_id="123")

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=True)
        manager.documents.create(template=template2, envelope_id="122", is_signed=False)
        manager1.documents.create(template=template, envelope_id='321', is_signed=True)
        manager1.documents.create(template=template2, envelope_id='324', is_signed=True)

        # Assert
        self.assertFalse(manager.is_all_documents_signed())
        self.assertTrue(manager1.is_all_documents_signed())


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
        HunterDocTemplateModel.objects.create(template_id=PRE_TOUR_TEMPLATE_ID)

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

    def test_is_pre_tour_signed_multiple_users_one_does_not_exist(self):
        """
        Tests that if there are different users, if one has it signed and one does not have a doc created,
            then the user that has it signed returns true and the other is false
        :return:
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        user1 = MyUser.objects.create(email="test@test1.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        manager1 = HunterDocManagerModel.objects.create(user=user1)
        template = HunterDocManagerModel.retrieve_pre_tour_template()

        # Act
        manager1.documents.create(template=template, envelope_id="123", is_signed=True)

        # Assert
        self.assertFalse(manager.is_pre_tour_signed())
        self.assertTrue(manager1.is_pre_tour_signed())

    def test_is_pre_tour_signed_multiple_users(self):
        """
        Tests that if each user has a pre tour document, then if one is signed and one isn't,
            the correct validation is returned from is_pre_tour_signed
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        user1 = MyUser.objects.create(email="test@test1.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        manager1 = HunterDocManagerModel.objects.create(user=user1)
        template = HunterDocManagerModel.retrieve_pre_tour_template()

        # Act
        manager.documents.create(template=template, envelope_id="123", is_signed=False)
        manager1.documents.create(template=template, envelope_id="123", is_signed=True)

        # Assert
        self.assertFalse(manager.is_pre_tour_signed())
        self.assertTrue(manager1.is_pre_tour_signed())

    def test_create_pre_tour_documents_send(self):
        """
        Tests that if the document is sent and the enevelope is retrieved then the document
            is created in the database
        """
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

    def test_create_pre_tour_documents_envelope_id_none(self):
        """
        Tests that if the docusign api for creating the envelope_id fails and none is returned,
            then create_pre_tour_documents returns false
        """
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com", first_name="TestName", last_name="TestLast")
        manager = HunterDocManagerModel.objects.create(user=user)
        DocusignLogin.set_up_docusign_api = MagicMock()
        DocusignWrapper.send_document_for_signatures = MagicMock(return_value=None)

        # Act
        result = manager.create_pre_tour_documents()

        # Assert
        self.assertFalse(result)

    def test_pre_tour_forms_created(self):
        """
        Tests that if a pretour document exists in the manager for that user then this will
            return true
        """
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com", first_name="TestName", last_name="TestLast")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.create_pre_tour_template()
        manager.documents.create(template=template)

        # Act
        result = manager.pre_tour_forms_created()

        # Assert
        self.assertTrue(result)

    def test_pre_tour_forms_created_wrong_user(self):
        """
        Tests that if one user has the pre_tour documents created and the other doesn't. Then
            there isn't any conflict across user accounts
        """
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com")
        user1 = MyUser.objects.create(email="awagud121@gmail.com")
        manager = HunterDocManagerModel.objects.create(user=user)
        manager1 = HunterDocManagerModel.objects.create(user=user1)
        template = HunterDocTemplateModel.create_pre_tour_template()
        manager.documents.create(template=template)

        # Act
        result = manager.pre_tour_forms_created()
        result1 = manager1.pre_tour_forms_created()

        # Assert
        self.assertTrue(result)
        self.assertFalse(result1)

    def test_resend_pre_tour_documents_exists(self):
        """
        Tests that if the user wants to resend the pre_tour_forms then if the document exists
            the document is sent
        """
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com", first_name="TestName", last_name="TestLast")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.create_pre_tour_template()
        doc = manager.documents.create(template=template, envelope_id='123')

        # Magic mock to prevent remote api call
        DocusignLogin.set_up_docusign_api = MagicMock()
        DocusignWrapper.resend_envelope = MagicMock(return_value=True)

        # Act
        result = manager.resend_pre_tour_documents()

        # Assert
        self.assertTrue(result)
        DocusignWrapper.resend_envelope.assert_called_once_with(doc.envelope_id)

    def test_resend_pre_tour_documents_not_exist(self):
        """
        Tests that if the user wants to resend the documents but the document doesn't exist,
            then it can't be sent and false is returned
        """
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com", first_name="TestName", last_name="TestLast")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.create_pre_tour_template()

        # Magic mock to prevent remote api call
        DocusignLogin.set_up_docusign_api = MagicMock()
        DocusignWrapper.resend_envelope = MagicMock(return_value=True)

        # Act
        result = manager.resend_pre_tour_documents()

        # Assert
        self.assertFalse(result)
        DocusignWrapper.resend_envelope.assert_not_called()

    def test_resend_pre_tour_documents_multiple_documents(self):
        """
        Tests that if the user wants to resend the documents but for some reason multiple
            documents are returned, then false is returned
        """
        # Arrange
        user = MyUser.objects.create(email="awagud12@gmail.com", first_name="TestName", last_name="TestLast")
        manager = HunterDocManagerModel.objects.create(user=user)
        template = HunterDocTemplateModel.create_pre_tour_template()
        doc = manager.documents.create(template=template, envelope_id='123')
        doc1 = manager.documents.create(template=template, envelope_id='321')

        # Magic mock to prevent remote api call
        DocusignLogin.set_up_docusign_api = MagicMock()
        DocusignWrapper.resend_envelope = MagicMock(return_value=True)

        # Act
        result = manager.resend_pre_tour_documents()

        # Assert
        self.assertFalse(result)
        DocusignWrapper.resend_envelope.assert_not_called()
