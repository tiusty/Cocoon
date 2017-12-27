# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from survey.forms import RentSurvey, HomeInformationForm, CommuteInformationForm, PriceInformationForm, \
    InteriorAmenitiesForm, ExteriorAmenitiesForm
from survey.models import HomeTypeModel

# Import cocoon global config values
from Unicorn.settings.Global_Config import MAX_NUM_BEDROOMS, WEIGHT_QUESTION_MAX


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

    def tests_home_information_form_max_num_bedrooms_missing(self):
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

    def tests_home_information_form_missing_min_num_bedrooms(self):
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

    def tests_home_information_form_min_bedrooms_less_than_zero(self):
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
        self.commute_type = 'driving'

    def tests_commute_information_valid(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': self.commute_weight,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_commute_information_max_commute_missing(self):
        # Arrange
        form_data = {
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': self.commute_weight,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_min_commute_missing(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'commute_weight_survey': self.commute_weight,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_missing(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_over_weight_question_max(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': WEIGHT_QUESTION_MAX + 1,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_under_zero(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': -1,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_type_missing(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': -1,
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestPriceInformationForm(TestCase):

    def setUp(self):
        self.max_price = 0
        self.min_price = 0
        self.price_weight = 0

    def tests_price_information_valid(self):
        # Arrange
        form_data = {
            'max_price_survey': self.max_price,
            'min_price_survey': self.min_price,
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
            'min_price_survey': self.min_price,
            'price_weight_survey': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_min_price_missing(self):
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
            'min_price_survey': self.min_price,
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
