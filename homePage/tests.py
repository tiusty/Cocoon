from django.test import TestCase

from homePage.forms import HomePageForm

# Create your tests here.


class HomePageFormTest(TestCase):
    def test_forms_correct_input(self):
        form_data = {
            'survey_type': 'buy',
            'streetAddress': '12 Stony Brook Rd',
            'city': 'Arlington',
            'state': 'MA',
            'zip_code': '02476-8019',
        }
        form = HomePageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_forms_empty_survey_type_field(self):
        form_data = {
            'streetAddress': '12 Stony Brook Rd',
            'city': 'Arlington',
            'state': 'MA',
            'zip_code': '02476-8019',
        }
        form = HomePageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_empty_streetAddress_field(self):
        form_data = {
            'survey_type': 'buy',
            'city': 'Arlington',
            'state': 'MA',
            'zip_code': '02476-8019',
        }
        form = HomePageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_empty_city_field(self):
        form_data = {
            'survey_type': 'buy',
            'streetAddress': '12 Stony Brook Rd',
            'state': 'MA',
            'zip_code': '02476-8019',
        }
        form = HomePageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_empty_state_field(self):
        form_data = {
            'survey_type': 'buy',
            'streetAddress': '12 Stony Brook Rd',
            'city': 'Arlington',
            'zip_code': '02476-8019',
        }
        form = HomePageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_empty_zip_code_field(self):
        form_data = {
            'survey_type': 'buy',
            'streetAddress': '12 Stony Brook Rd',
            'city': 'Arlington',
            'state': 'MA',
        }
        form = HomePageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_radio_select_buy(self):
        form_data = {
            'survey_type': 'buy',
            'streetAddress': '12 Stony Brook Rd',
            'city': 'Arlington',
            'state': 'MA',
            'zip_code': '02476-8019',
        }
        form = HomePageForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['survey_type'], 'buy')

    def test_forms_radio_select_rent(self):
        form_data = {
            'survey_type': 'rent',
            'streetAddress': '12 Stony Brook Rd',
            'city': 'Arlington',
            'state': 'MA',
            'zip_code': '02476-8019',
        }
        form = HomePageForm(data=form_data)
        form.is_valid()
        self.assertEquals(form.cleaned_data['survey_type'], 'rent')