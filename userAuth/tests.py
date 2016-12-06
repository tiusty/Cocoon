from django.test import TestCase

# Create your tests here.

from userAuth.forms import RegisterForm,LoginForm


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

    def test_form_different_passwords(self):
        form_data = {
            'first_name': 'Alex',
            'last_name': 'Agudelo',
            'email': 'email@test.com',
            'password1': 'sometestPassword',
            'password2': 'sometestPasswordDifferent',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid)