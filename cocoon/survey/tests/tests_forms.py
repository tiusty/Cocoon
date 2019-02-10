# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from cocoon.survey.forms import RentSurveyForm, HomeInformationForm, CommuteInformationForm, PriceInformationForm, \
    ExteriorAmenitiesForm, InteriorAmenitiesForm, HouseNearbyAmenitiesForm, RentSurveyFormEdit
from cocoon.survey.models import RentingSurveyModel
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType
from cocoon.userAuth.models import MyUser
from ..constants import MOVE_WEIGHT_MAX


class TestHomeInformationForm(TestCase):

    def setUp(self):
        # Create home type objects
        HomeTypeModel.objects.create(home_type="Apartment")

    def tests_home_information_form_valid_not_max_weight(self):
        """
        Tests valid form with requiring earliest_move_in and latest move in
        """
        home_type = [HomeTypeModel.objects.get(home_type="Apartment")]
        # Arrange
        form_data = {
            'num_bedrooms': 0,
            'home_type': home_type,
            'polygon_filter_type': 1,
            'move_weight': 0,
            'latest_move_in': timezone.now(),
            'earliest_move_in': timezone.now(),
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_home_information_form_valid_max_weight(self):
        """
        Tests valid form with requiring earliest_move_in and latest move in
        """
        home_type = [HomeTypeModel.objects.get(home_type="Apartment")]
        # Arrange
        form_data = {
            'num_bedrooms': 0,
            'home_type': home_type,
            'polygon_filter_type': 1,
            'move_weight': MOVE_WEIGHT_MAX,
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_home_information_form_missing_earliest_move_in_not_max_weight(self):
        """
        Tests that if the move_weight is not max, then the earliest move in is required
        """
        home_type = [HomeTypeModel.objects.get(home_type="Apartment")]
        # Arrange
        form_data = {
            'num_bedrooms': 0,
            'home_type': home_type,
            'polygon_filter_type': 1,
            'move_weight': MOVE_WEIGHT_MAX-1,
            'earliest_move_in': timezone.now(),
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_missing_latest_move_in_not_max_weight(self):
        """
        Tests that if the move_weight is not max, then the latest move in is required
        """
        home_type = [HomeTypeModel.objects.get(home_type="Apartment")]
        # Arrange
        form_data = {
            'num_bedrooms': 0,
            'home_type': home_type,
            'polygon_filter_type': 1,
            'move_weight': MOVE_WEIGHT_MAX-1,
            'latest_move_in': timezone.now(),
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestCommuteInformationForm(TestCase):

    def setUp(self):
        self.max_commute = 0
        self.min_commute = 0
        self.commute_weight = 1
        self.driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        self.bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        self.transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)
        self.walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        self.work_from_home = CommuteType.objects.create(commute_type=CommuteType.WORK_FROM_HOME)

    def tests_commute_information_valid_not_work_from_home(self):
        """
        Tests that given all the required fields the commute form validates for all the
        commute types besides work from home
        """

        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertTrue(result)

    def tests_commute_information_street_address_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if street address is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_city_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if city is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_state_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if the state is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_zip_code_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if the zip_code is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_commute_weight_not_work_from_home(self):
        """
        Tests that if min_commute is missing and the commute type is not work from home then the form
            returns False
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_max_commute_not_work_from_home(self):
        """
        Tests that if max_commute is missing and the commute type is not work from home then the form
            returns False
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_min_commute_less_than_zero_not_work_from_home(self):
        """
        Tests that if the min_commute is less than zero and the commute types is not work from home
            then valid is false
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'desired_commute': -1,
                'commute_weight': 1,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_max_commute_less_than_zero_not_work_from_home(self):
        """
        Tests that if the max_commute is less than zero and the commute types is not work from home
            then valid is false
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': -1,
                'min_commute': self.min_commute,
                'commute_weight': 1,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_max_commute_less_than_min_commute_not_work_from_home(self):
        """
        Tests that if the max_commute is less than min_commute and the commute types is not work from home
            then valid is false
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': 1,
                'desired_commute': 2,
                'commute_weight': 1,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_valid_work_from_home(self):
        """
        Tests that work from home doesn't need any other fields to validate
        """

        # Arrange
        form_data = {
            'commute_type': self.work_from_home.pk,
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertTrue(result)
