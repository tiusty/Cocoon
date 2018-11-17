# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from cocoon.survey.forms import RentSurveyForm, HomeInformationForm, CommuteInformationForm, PriceInformationForm, \
    ExteriorAmenitiesForm, RentSurveyFormMini
from cocoon.survey.models import RentingSurveyModel
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType
from cocoon.userAuth.models import MyUser

# Import cocoon global config values
from config.settings.Global_Config import WEIGHT_QUESTION_MAX, MAX_NUM_BATHROOMS


class TestHomeInformationForm(TestCase):

    def setUp(self):

        # Create home type objects
        HomeTypeModel.objects.create(home_type="Apartment")
        HomeTypeModel.objects.create(home_type="Condo")
        HomeTypeModel.objects.create(home_type="Town House")
        HomeTypeModel.objects.create(home_type="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type = [HomeTypeModel.objects.get(home_type="Apartment")]

    def tests_home_information_form_valid(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type
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

    def tests_home_information_form_num_bedrooms_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type
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
            'num_bedrooms': -1,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_max_num_bathrooms_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_num_bedrooms_more_than_max_num_bathrooms(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': MAX_NUM_BATHROOMS + 1,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_missing_min_num_bathrooms(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'home_type': self.home_type
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_min_bathrooms_less_than_zero(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': -1,
            'home_type': self.home_type
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_home_type_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': -1,
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
        self.commute_weight = 0
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

    def tests_commute_information_missing_min_commute_not_work_from_home(self):
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
                'min_commute': -1,
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
                'min_commute': 2,
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


class TestPriceInformationForm(TestCase):

    def setUp(self):
        self.max_price = 0
        self.desired_price = 0
        self.price_weight = 0

    def tests_price_information_valid(self):
        # Arrange
        form_data = {
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_price_information_max_price_missing(self):
        # Arrange
        form_data = {
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_desired_price_missing(self):
        # Arrange
        form_data = {
            'max_price': self.max_price,
            'price_weight': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_price_weight_missing(self):
        # Arrange
        form_data = {
            'max_price': self.max_price,
            'desired_price': self.desired_price,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestExteriorAmenitiesForm(TestCase):

    def setUp(self):
        self.parking_spot = 0
        self.building_washer_dryer = 0
        self.elevator = 0
        self.handicap_access = 0
        self.pool_hot_tub = 0
        self.fitness_center = 0
        self.storage_unit = 0

    def tests_exterior_amenities_valid(self):
        # Arrange
        form_data = {
            'parking_spot': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'fitness_center_survey': self.fitness_center,
            'storage_unit_survey': self.storage_unit
        }
        exterior_amenities_form = ExteriorAmenitiesForm(data=form_data)

        # Act
        result = exterior_amenities_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_exterior_amenities_parking_spot_missing(self):
        # Arrange
        form_data = {
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'fitness_center_survey': self.fitness_center,
            'storage_unit_survey': self.storage_unit
        }
        exterior_amenities_form = ExteriorAmenitiesForm(data=form_data)

        # Act
        result = exterior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestRentSurveyForm(TestCase):

    def setUp(self):
        # Create home type objects
        HomeTypeModel.objects.create(home_type="Apartment")
        HomeTypeModel.objects.create(home_type="Condo")
        HomeTypeModel.objects.create(home_type="Town House")
        HomeTypeModel.objects.create(home_type="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type = [HomeTypeModel.objects.get(home_type="Apartment")]

        self.max_commute = 0
        self.min_commute = 0
        self.commute_weight = 0
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)

        self.max_price = 0
        self.desired_price = 0
        self.price_weight = 0

        self.air_conditioning = 0
        self.interior_washer_dryer = 0
        self.dish_washer = 0
        self.bath = 0

        self.parking_spot = 0
        self.building_washer_dryer = 0
        self.elevator = 0
        self.handicap_access = 0
        self.pool_hot_tub = 0
        self.fitness_center = 0
        self.storage_unit = 0

        self.number_of_destinations = 1

    def tests_rent_survey_valid(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'number_destinations_filled_out': self.number_of_destinations,
            'commute_type': 1,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'parking_spot': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'fitness_center_survey': self.fitness_center,
            'storage_unit_survey': self.storage_unit,
            'number_of_tenants': 2
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()
        print(rent_survey_form.errors)

        # Assert
        self.assertTrue(result)

    def tests_rent_survey_missing_home_information_data(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'parking_spot': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'fitness_center_survey': self.fitness_center,
            'storage_unit_survey': self.storage_unit
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_rent_survey_missing_price_information_data(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'parking_spot': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'fitness_center_survey': self.fitness_center,
            'storage_unit_survey': self.storage_unit
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_rent_survey_missing_exterior_amenities_data(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestRentSurveyMiniForm(TestCase):

    def setUp(self):

        # Creating user
        self.user = MyUser.objects.create()

        # Create home type objects
        HomeTypeModel.objects.create(home_type="Apartment")
        HomeTypeModel.objects.create(home_type="Condo")
        HomeTypeModel.objects.create(home_type="Town House")
        HomeTypeModel.objects.create(home_type="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type = [HomeTypeModel.objects.get(home_type="Apartment")]

        self.max_commute = 0
        self.min_commute = 0
        self.commute_weight = 0
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)

        self.max_price = 0
        self.desired_price = 0
        self.price_weight = 0

        self.air_conditioning = 0
        self.interior_washer_dryer = 0
        self.dish_washer = 0
        self.bath = 0

        self.parking_spot = 0
        self.building_washer_dryer = 0
        self.elevator = 0
        self.handicap_access = 0
        self.pool_hot_tub = 0
        self.fitness_center = 0
        self.storage_unit = 0

        self.number_of_destinations = 1

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2, name="Recent Rent Survey"):
        return RentingSurveyModel.objects.create(
            name=name,
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    def tests_saving_a_form_without_name_conflict(self):
        """
        Test that is there is no name conflict, the survey saves successfully
        """
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'fitness_center_survey': self.fitness_center,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'home_type': self.home_type,
            'storage_unit_survey': self.storage_unit,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'parking_spot': self.parking_spot,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'name': 'test_survey',
        }

        rent_survey_form = RentSurveyFormMini(data=form_data, user=self.user)

        # Act
        result = rent_survey_form.is_valid()
        print(rent_survey_form.errors)

        # Assert
        self.assertTrue(result)

    def tests_saving_a_form_with_name_conflict(self):
        """
        Tests that if a naming conflict occurs, i.e trying to save a survey with a survey with
            the same slug, then prevent the saving
        """
        # Arrange
        self.create_survey(self.user.userProfile, name='test_survey')

        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'fitness_center_survey': self.fitness_center,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'home_type': self.home_type,
            'storage_unit_survey': self.storage_unit,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'parking_spot': self.parking_spot,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'name': 'test_survey',
        }

        rent_survey_form = RentSurveyFormMini(data=form_data, user=self.user)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_saving_a_form_with_name_conflict_different_users(self):
        """
        Tests that if there is a naming conflict but with a different user, then allow the saving
        """
        # Arrange
        self.create_survey(self.user.userProfile, name='test_survey')
        user2 = MyUser.objects.create()

        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'fitness_center_survey': self.fitness_center,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'home_type': self.home_type,
            'storage_unit_survey': self.storage_unit,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'parking_spot': self.parking_spot,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'name': 'test_survey',
        }

        rent_survey_form = RentSurveyFormMini(data=form_data, user=user2)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertTrue(result)
