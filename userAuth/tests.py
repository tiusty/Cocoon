from django.test import TestCase

from userAuth.forms import RegisterForm,LoginUserForm

# Import cocoon global config
from Cocoon.settings.Global_Config import creation_key_value


class TestRegisterForm(TestCase):

    def setUp(self):
        self.first_name = 'Alex'
        self.last_name = 'Agudelo'
        self.username = 'email@text.com'
        self.password1 = 'sometestPassword'
        self.password2 = 'sometestPassword'
        self.creation_key = creation_key_value

    def tests_register_form_valid(self):
        # Arrange
        form_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.username,
            'password1': self.password1,
            'password2': self.password1,
            'creation_key': self.creation_key
        }

        # Act
        form = RegisterForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())


class TestLoginUserForm(TestCase):

    def setUp(self):
        # Login form data
        self.username = 'email@text.com'
        self.password = 'somePassword'
        self.remember = True

        # Register form data
        self.first_name = 'Alex'
        self.last_name = 'Agudelo'
        self.creation_key = creation_key_value

    def tests_login_user_form_valid(self):
        # Arrange

        # First create a user so that it can be logged into later
        register_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.username,
            'password1': self.password,
            'password2': self.password,
            'creation_key': self.creation_key
        }
        register_form = RegisterForm(data=register_data)
        register_form.is_valid()
        register_form.save()

        form_data = {
            'username': self.username,
            'password': self.password,
            'remember': self.remember,
        }

        # Act
        form = LoginUserForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def tests_login_user_form_username_missing(self):
        # Arrange
        form_data = {
            'password': self.password,
            'remember': self.remember,
        }

        # Act
        form = LoginUserForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def tests_login_user_form_password_missing(self):
        # Arrange
        form_data = {
            'username': self.username,
            'remember': self.remember,
        }

        # Act
        form = LoginUserForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
