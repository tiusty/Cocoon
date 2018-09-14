# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from cocoon.survey.forms import RentSurveyForm, HomeInformationForm, CommuteInformationForm, PriceInformationForm, \
    InteriorAmenitiesForm, ExteriorAmenitiesForm, RentSurveyFormMini
from cocoon.survey.models import RentingSurveyModel
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType
from cocoon.userAuth.models import MyUser

# Import cocoon global config values
from config.settings.Global_Config import WEIGHT_QUESTION_MAX, MAX_NUM_BATHROOMS


class TestHomeInformationForm(TestCase):

    def setUp(self):

        # Create home type objects
        HomeTypeModel.objects.create(home_type_survey="Apartment")
        HomeTypeModel.objects.create(home_type_survey="Condo")
        HomeTypeModel.objects.create(home_type_survey="Town House")
        HomeTypeModel.objects.create(home_type_survey="House")

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
            'num_bedrooms_survey': -1,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
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
            'num_bedrooms_survey': self.num_bedrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': MAX_NUM_BATHROOMS + 1,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'home_type_survey': self.home_type_survey
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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': -1,
            'home_type_survey': self.home_type_survey
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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': -1,
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
        self.commute_type = CommuteType.objects.create(commute_type='Driving')

    def tests_commute_information_valid(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type.pk,
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()
        print(commute_information_form.errors)

        # Assert
        self.assertTrue(result)

    def tests_commute_information_max_commute_missing(self):
        # Arrange
        form_data = {
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_min_commute_missing(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_missing(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_type': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_over_weight_question_max(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': WEIGHT_QUESTION_MAX + 1,
            'commute_type': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_under_zero(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': -1,
            'commute_type': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_type_missing(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': -1,
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestPriceInformationForm(TestCase):

    def setUp(self):
        self.max_price = 0
        self.desired_price = 0
        self.price_weight = 0

    def tests_price_information_valid(self):
        # Arrange
        form_data = {
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_price_information_max_price_missing(self):
        # Arrange
        form_data = {
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_desired_price_missing(self):
        # Arrange
        form_data = {
            'max_price_survey': self.max_price,
            'price_weight_survey': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_price_weight_missing(self):
        # Arrange
        form_data = {
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestInteriorAmenitiesForm(TestCase):

    def setUp(self):
        self.air_conditioning = 0
        self.interior_washer_dryer = 0
        self.dish_washer = 0
        self.bath = 0

    def tests_interior_amenities_valid(self):
        # Arrange
        form_data = {
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath
        }
        interior_amenities_form = InteriorAmenitiesForm(data=form_data)

        # Act
        result = interior_amenities_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_interior_amenities_air_conditioning_missing(self):
        # Arrange
        form_data = {
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath
        }
        interior_amenities_form = InteriorAmenitiesForm(data=form_data)

        # Act
        result = interior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_interior_amenities_interior_washer_dryer_missing(self):
        # Arrange
        form_data = {
            'air_conditioning_survey': self.air_conditioning,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath
        }
        interior_amenities_form = InteriorAmenitiesForm(data=form_data)

        # Act
        result = interior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_interior_amenities_dish_washer_missing(self):
        # Arrange
        form_data = {
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'bath_survey': self.bath
        }
        interior_amenities_form = InteriorAmenitiesForm(data=form_data)

        # Act
        result = interior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_interior_amenities_bath_missing(self):
        # Arrange
        form_data = {
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'bath_survey': self.bath
        }
        interior_amenities_form = InteriorAmenitiesForm(data=form_data)

        # Act
        result = interior_amenities_form.is_valid()

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
            'parking_spot_survey': self.parking_spot,
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

    def tests_exterior_amenities_building_washer_dryer_missing(self):
        # Arrange
        form_data = {
            'parking_spot_survey': self.parking_spot,
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

    def tests_exterior_amenities_elevator_missing(self):
        # Arrange
        form_data = {
            'parking_spot_survey': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
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

    def tests_exterior_amenities_handicap_access_missing(self):
        # Arrange
        form_data = {
            'parking_spot_survey': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'fitness_center_survey': self.fitness_center,
            'storage_unit_survey': self.storage_unit
        }
        exterior_amenities_form = ExteriorAmenitiesForm(data=form_data)

        # Act
        result = exterior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_exterior_amenities_pool_hot_tub_missing(self):
        # Arrange
        form_data = {
            'parking_spot_survey': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'fitness_center_survey': self.fitness_center,
            'storage_unit_survey': self.storage_unit
        }
        exterior_amenities_form = ExteriorAmenitiesForm(data=form_data)

        # Act
        result = exterior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_exterior_amenities_fitness_center_missing(self):
        # Arrange
        form_data = {
            'parking_spot_survey': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'storage_unit_survey': self.storage_unit
        }
        exterior_amenities_form = ExteriorAmenitiesForm(data=form_data)

        # Act
        result = exterior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_exterior_amenities_storage_unit_missing(self):
        # Arrange
        form_data = {
            'parking_spot_survey': self.parking_spot,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'fitness_center_survey': self.fitness_center,
        }
        exterior_amenities_form = ExteriorAmenitiesForm(data=form_data)

        # Act
        result = exterior_amenities_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestRentSurveyForm(TestCase):

    def setUp(self):
        # Create home type objects
        HomeTypeModel.objects.create(home_type_survey="Apartment")
        HomeTypeModel.objects.create(home_type_survey="Condo")
        HomeTypeModel.objects.create(home_type_survey="Town House")
        HomeTypeModel.objects.create(home_type_survey="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type_survey = [HomeTypeModel.objects.get(home_type_survey="Apartment")]

        self.max_commute = 0
        self.min_commute = 0
        self.commute_weight = 0
        self.commute_type = CommuteType.objects.create(commute_type='Driving')

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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'number_destinations_filled_out': self.number_of_destinations,
            'commute_type': 1,
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'parking_spot_survey': self.parking_spot,
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
        self.assertTrue(result)

    def tests_rent_survey_missing_home_information_data(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'parking_spot_survey': self.parking_spot,
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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'parking_spot_survey': self.parking_spot,
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

    def tests_rent_survey_missing_interior_amenities_data(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
            'parking_spot_survey': self.parking_spot,
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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
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
        self.user = MyUser.objects.create(email="test@email.com")

        # Create home type objects
        HomeTypeModel.objects.create(home_type_survey="Apartment")
        HomeTypeModel.objects.create(home_type_survey="Condo")
        HomeTypeModel.objects.create(home_type_survey="Town House")
        HomeTypeModel.objects.create(home_type_survey="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type_survey = [HomeTypeModel.objects.get(home_type_survey="Apartment")]

        self.max_commute = 0
        self.min_commute = 0
        self.commute_weight = 0
        self.commute_type = CommuteType.objects.create(commute_type='Driving')

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
            name_survey=name,
            user_profile_survey=user_profile,
            max_price_survey=max_price,
            desired_price_survey=desired_price,
            max_bathrooms_survey=max_bathroom,
            min_bathrooms_survey=min_bathroom,
            num_bedrooms_survey=num_bedrooms,
        )

    def tests_saving_a_form_without_name_conflict(self):
        """
        Test that is there is no name conflict, the survey saves successfully
        """
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'fitness_center_survey': self.fitness_center,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'home_type_survey': self.home_type_survey,
            'storage_unit_survey': self.storage_unit,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'parking_spot_survey': self.parking_spot,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'name_survey': 'test_survey',
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
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'fitness_center_survey': self.fitness_center,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'home_type_survey': self.home_type_survey,
            'storage_unit_survey': self.storage_unit,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'parking_spot_survey': self.parking_spot,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'name_survey': 'test_survey',
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
        user2 = MyUser.objects.create(email="test2@gmail.com")

        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'max_price_survey': self.max_price,
            'desired_price_survey': self.desired_price,
            'price_weight_survey': self.price_weight,
            'air_conditioning_survey': self.air_conditioning,
            'interior_washer_dryer_survey': self.interior_washer_dryer,
            'dish_washer_survey': self.dish_washer,
            'bath_survey': self.bath,
            'fitness_center_survey': self.fitness_center,
            'building_washer_dryer_survey': self.building_washer_dryer,
            'home_type_survey': self.home_type_survey,
            'storage_unit_survey': self.storage_unit,
            'pool_hot_tub_survey': self.pool_hot_tub,
            'parking_spot_survey': self.parking_spot,
            'elevator_survey': self.elevator,
            'handicap_access_survey': self.handicap_access,
            'name_survey': 'test_survey',
        }

        rent_survey_form = RentSurveyFormMini(data=form_data, user=user2)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertTrue(result)
