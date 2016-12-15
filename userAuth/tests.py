from django.test import TestCase

# Create your tests here.

from userAuth.forms import RegisterForm,LoginUserForm


class RegisterFormTest(TestCase):
    def test_form_correct_input(self):
        form_data = {
            'first_name': 'Alex',
            'last_name': 'Agudelo',
            'email': 'email@test.com',
            'password1': 'sometestPassword',
            'password2': 'sometestPassword',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())


class LoginFormTest(TestCase):
    def test_form_correct_input_with_remember(self):
        form_data = {
            'username': 'email@text.com',
            'password': 'somePassword',
            'remember': 'True',
        }
        form = LoginUserForm(data=form_data)
        self.assertTrue(form.is_valid)
