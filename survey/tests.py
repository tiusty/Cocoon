# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from survey.forms import RentSurvey, HomeInformationForm
from survey.models import HomeTypeModel


class TestRentSurveyForm(TestCase):

    def setUp(self):
        HomeTypeModel.objects.create(home_type_survey="Apartment")
        HomeTypeModel.objects.create(home_type_survey="Condo")
        HomeTypeModel.objects.create(home_type_survey="Town House")
        HomeTypeModel.objects.create(home_type_survey="House")
        self.default_home_type = ['2']
        self.commute_type = "driving"

    def tests_home_information_form(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': timezone.now(),
            'move_in_date_end_survey': timezone.now(),
            'num_bedrooms_survey': 2,
            'max_bathrooms_survey': 0,
            'min_bathrooms_survey': 0,
            'home_type_survey': [HomeTypeModel.objects.get(home_type_survey="Apartment")]
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertTrue(result)
