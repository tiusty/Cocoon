from django.test import TestCase

# Import Cocoon Modules
from cocoon.userAuth.constants import BROKER_CREATION_KEY
from cocoon.userAuth.forms import ApartmentHunterSignupForm, BrokerSignupForm


class TestApartmentHunterSignupForm(TestCase):

    def tests_form_valid(self):
        """
        Tests that given the correct info the form will validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_form_not_matching_passwords(self):
        """
        Tests that given non-matching passwords, the form will not validate
        :return:
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword1'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'password2': ["The two password fields didn't match."]}, form.errors)

    def test_form_email_not_valid(self):
        """
        Tests that if the email field is not a valid email, the form will not validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'email': ['Enter a valid email address.']}, form.errors)


class TTestApartmentHunterSignupForm(TestCase):

    def tests_form_valid(self):
        """
        Tests that given the correct info the form will validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'
        creation_key = BROKER_CREATION_KEY

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_form_wrong_key(self):
        """
        Tests thta given the wrong key the form doesn't validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'
        creation_key = 'some_random_key'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'creation_key': ['Creation Key invaild']}, form.errors)

    def test_form_not_matching_passwords(self):
        """
        Tests that given non-matching passwords, the form will not validate
        :return:
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword1'
        creation_key = BROKER_CREATION_KEY

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'password2': ["The two password fields didn't match."]}, form.errors)

    def test_form_email_not_valid(self):
        """
        Tests that if the email field is not a valid email, the form will not validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'
        creation_key = BROKER_CREATION_KEY

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'email': ['Enter a valid email address.']}, form.errors)
