# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from survey.forms import RentSurvey, HomeInformationForm
from survey.models import HomeTypeModel

# Import cocoon global config values
from Unicorn.settings.Global_Config import MAX_NUM_BEDROOMS


class TestHomeInformationForm(TestCase):

    def setUp(self):
        HomeTypeModel.objects.create(home_type_survey="Apartment")
        HomeTypeModel.objects.create(home_type_survey="Condo")
        HomeTypeModel.objects.create(home_type_survey="Town House")
        HomeTypeModel.objects.create(home_type_survey="House")
        self.default_home_type = ['2']
        self.commute_type = "driving"
        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type_survey = [HomeTypeModel.objects.get(home_type_survey="Apartment")]

    def tests_home_information_form_valid(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_home_information_form_not_valid(self):
        # Arrange
        form_data = {}

        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_start_missing(self):
        # Arrange
        form_data = {
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_start_not_valid_in_past(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': timezone.now() + timezone.timedelta(days=-1),
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_end_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_end_before_start_date(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': timezone.now() + timezone.timedelta(days=-1),
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_num_bedrooms_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_num_bedrooms_less_than_one(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': 0,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_num_bedrooms_more_than_max_num_bedrooms(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': MAX_NUM_BEDROOMS + 1,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

