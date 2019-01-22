from django.test import TestCase
from unittest import skip
from django.utils import timezone
from unittest.mock import MagicMock, Mock, patch, call

# Import Google geolocator
import cocoon.houseDatabase.maps_requester as geolocator

# Import external models
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, HomeProviderModel
from cocoon.commutes.distance_matrix import commute_cache_updater
from cocoon.commutes.models import ZipCodeBase, CommuteType
from cocoon.commutes.constants import CommuteAccuracy
# Import survey python modules
from cocoon.survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from cocoon.survey.home_data.home_score import HomeScore
from cocoon.survey.models import RentingSurveyModel
from cocoon.userAuth.models import MyUser, UserProfile

from cocoon.survey.constants import AVERAGE_BICYCLING_SPEED, AVERAGE_WALKING_SPEED


class TestRentAlgorithmJustApproximateCommuteFilter(TestCase):

    def setUp(self):
        # Create a commute type
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        HomeProviderModel.objects.create(provider="MLSPIN")
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile=self.user_profile)

        # Add renting destination
        self.street_address = '12 Stony Brook Rd'
        self.city = 'Arlington'
        self.state = 'MA'
        self.zip_code = '02476'
        self.commute_type = self.commute_type
        self.commute_weight = 0

        self.street_address1 = '8 Stony Brook Rd'
        self.city1 = 'Arlington'
        self.state1 = 'MA'
        self.zip_code1 = '02476'
        self.commute_type1 = self.commute_type
        self.commute_weight1 = 1
        self.home_type = HomeTypeModel.objects.create(home_type='House')

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    def test_run_compute_approximate_commute_filter_no_eliminations(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.approx_commute_range = 20

        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the first commuter destination
        self.min_commute = 20
        self.max_commute = 80
        self.destination = self.survey.tenants.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Create the second commuter destination
        self.min_commute1 = 40
        self.max_commute1 = 90
        self.destination1 = self.survey.tenants.create(
            street_address=self.street_address1,
            city=self.city1,
            state=self.state1,
            zip_code=self.zip_code1,
            commute_type=self.commute_type1,
            commute_weight=self.commute_weight1,
            max_commute=self.max_commute1,
            min_commute=self.min_commute1,
        )

        # Set commutes times from each home to the each commuters destination
        self.home.approx_commute_times = {self.destination: 50}
        self.home.approx_commute_times = {self.destination1: 70}

        self.home1.approx_commute_times = {self.destination: 10}
        self.home1.approx_commute_times = {self.destination1: 70}

        self.home2.approx_commute_times = {self.destination: 40}
        self.home2.approx_commute_times = {self.destination1: 100}

        # Create homes
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertFalse(rent_algorithm.homes[0].eliminated)
        self.assertFalse(rent_algorithm.homes[1].eliminated)
        self.assertFalse(rent_algorithm.homes[2].eliminated)

    def test_run_compute_approximate_commute_filter_one_elimination(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.approx_commute_range = 10
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the first commuter destination
        self.min_commute = 20
        self.max_commute = 60
        self.destination = self.survey.tenants.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Create the second commuter destination
        self.min_commute1 = 10
        self.max_commute1 = 80
        self.destination1 = self.survey.tenants.create(
            street_address=self.street_address1,
            city=self.city1,
            state=self.state1,
            zip_code=self.zip_code1,
            commute_type=self.commute_type1,
            commute_weight=self.commute_weight1,
            max_commute=self.max_commute1,
            min_commute=self.min_commute1,
        )

        # Set commutes times from each home to the each commuters destination
        self.home.approx_commute_times = {self.destination: 50}
        self.home.approx_commute_times = {self.destination1: 70}

        self.home1.approx_commute_times = {self.destination: 10}
        self.home1.approx_commute_times = {self.destination1: 70}

        self.home2.approx_commute_times = {self.destination: 40}
        self.home2.approx_commute_times = {self.destination1: 100}

        # Create homes
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertFalse(rent_algorithm.homes[0].eliminated)
        self.assertFalse(rent_algorithm.homes[1].eliminated)
        self.assertTrue(rent_algorithm.homes[2].eliminated)

    def test_run_compute_approximate_commute_filter_all_eliminated(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.approx_commute_range = 0
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the first commuter destination
        self.min_commute = 60
        self.max_commute = 60
        self.destination = self.survey.tenants.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Create the second commuter destination
        self.min_commute1 = 80
        self.max_commute1 = 80
        self.destination1 = self.survey.tenants.create(
            street_address=self.street_address1,
            city=self.city1,
            state=self.state1,
            zip_code=self.zip_code1,
            commute_type=self.commute_type1,
            commute_weight=self.commute_weight1,
            max_commute=self.max_commute1,
            min_commute=self.min_commute1,
        )

        # Set commutes times from each home to the each commuters destination
        self.home.approx_commute_times = {self.destination: 50}
        self.home.approx_commute_times = {self.destination1: 70}

        self.home1.approx_commute_times = {self.destination: 10}
        self.home1.approx_commute_times = {self.destination1: 70}

        self.home2.approx_commute_times = {self.destination: 40}
        self.home2.approx_commute_times = {self.destination1: 100}

        # Create homes
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertTrue(rent_algorithm.homes[0].eliminated)
        self.assertTrue(rent_algorithm.homes[1].eliminated)
        self.assertTrue(rent_algorithm.homes[2].eliminated)

    def test_run_compute_approximate_commute_filter_one_destination_out_of_range(self):
        """
        This unit tests tests for a given home, if one of the destinations is out of range
            but the other one is in range, the home is still marked for elimination
        :return:
        """
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.approx_commute_range = 20
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the first commuter destination
        self.min_commute = 20
        self.max_commute = 80
        self.destination = self.survey.tenants.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Create the second commuter destination
        self.min_commute1 = 30
        self.max_commute1 = 60
        self.destination1 = self.survey.tenants.create(
            street_address=self.street_address1,
            city=self.city1,
            state=self.state1,
            zip_code=self.zip_code1,
            commute_type=self.commute_type1,
            commute_weight=self.commute_weight1,
            max_commute=self.max_commute1,
            min_commute=self.min_commute1,
        )

        # Set commutes times from each home to the each commuters destination
        self.home.approx_commute_times = {self.destination: 50}
        self.home.approx_commute_times = {self.destination1: 90}

        self.home1.approx_commute_times = {self.destination: 10}
        self.home1.approx_commute_times = {self.destination1: 70}

        self.home2.approx_commute_times = {self.destination: 120}
        self.home2.approx_commute_times = {self.destination1: 80}

        # Create homes
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertTrue(rent_algorithm.homes[0].eliminated)
        self.assertFalse(rent_algorithm.homes[1].eliminated)
        self.assertTrue(rent_algorithm.homes[2].eliminated)

    def test_run_compute_approximate_commute_filter_no_homes(self):
        # Arrange
        rent_algorithm = RentAlgorithm()

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertEqual(0, len(rent_algorithm.homes))


class TestRentAlgorithmJustPrice(TestCase):

    def setUp(self):
        CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        HomeProviderModel.objects.create(provider="MLSPIN")
        self.home_type = HomeTypeModel.objects.create(home_type='House')

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    def test_run_compute_price_score_working(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type, price=1000)
        self.home1 = self.create_home(self.home_type, price=1500)
        self.home2 = self.create_home(self.home_type, price=2000)
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.desired_price = 1000
        rent_algorithm.max_price = 2500

        # Set the user scale
        price_user_scale_factor = 1
        rent_algorithm.price_user_scale_factor = price_user_scale_factor
        # Overriding in case the config file changes
        price_question_weight = 100
        rent_algorithm.price_question_weight = price_question_weight

        # Act
        rent_algorithm.run_compute_price_score()

        # Assert
        self.assertEqual((1 - (0 / 1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertFalse(rent_algorithm.homes[0].eliminated)
        self.assertEqual((1 - (500 / 1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)
        self.assertEqual((1 - (1000 / 1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertFalse(rent_algorithm.homes[2].eliminated)

    def test_run_compute_price_score_one_elimination_desired_price(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type, price=1000)
        self.home1 = self.create_home(self.home_type, price=1500)
        self.home2 = self.create_home(self.home_type, price=2000)
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1100
        rent_algorithm.desired_price = 1400
        rent_algorithm.max_price = 2500

        # Set the user scale
        price_user_scale_factor = 1
        rent_algorithm.price_user_scale_factor = price_user_scale_factor
        # Overriding in case the config file changes
        price_question_weight = 100
        rent_algorithm.price_question_weight = price_question_weight

        # Act
        rent_algorithm.run_compute_price_score()

        # Assert

        # Home 0
        self.assertEqual(-100, rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertTrue(rent_algorithm.homes[0].eliminated)

        # Home 1
        self.assertEqual((1 - (100 / 1100)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual((1 - (600 / 1100)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertFalse(rent_algorithm.homes[2].eliminated)

    def test_run_compute_price_score_two_eliminations_min_price(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type, price=1000)
        self.home1 = self.create_home(self.home_type, price=1500)
        self.home2 = self.create_home(self.home_type, price=2000)
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1600
        rent_algorithm.desired_price = 1900
        rent_algorithm.max_price = 2500

        # Set the user scale
        price_user_scale_factor = 1
        rent_algorithm.price_user_scale_factor = price_user_scale_factor
        # Overriding in case the config file changes
        price_question_weight = 100
        rent_algorithm.price_question_weight = price_question_weight

        # Act
        rent_algorithm.run_compute_price_score()

        # Assert

        # Home 0
        self.assertEqual(-100, rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertTrue(rent_algorithm.homes[0].eliminated)

        # Home 1
        self.assertEqual(-100, rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertTrue(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual((1 - (100 / 600)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertFalse(rent_algorithm.homes[2].eliminated)

    def test_run_compute_price_score_one_elimination_max_price(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type, price=1000)
        self.home1 = self.create_home(self.home_type, price=1500)
        self.home2 = self.create_home(self.home_type, price=2000)
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.desired_price = 1000
        rent_algorithm.max_price = 1900

        # Set the user scale
        price_user_scale_factor = 1
        rent_algorithm.price_user_scale_factor = price_user_scale_factor
        # Overriding in case the config file changes
        price_question_weight = 100
        rent_algorithm.price_question_weight = price_question_weight

        # Act
        rent_algorithm.run_compute_price_score()

        # Assert

        # Home 0
        self.assertEqual((1 - (0 / 900)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertFalse(rent_algorithm.homes[0].eliminated)

        # Home 1
        self.assertEqual((1 - (500 / 900)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual(-100, rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].total_possible_points)
        self.assertTrue(rent_algorithm.homes[2].eliminated)

    def test_run_compute_price_score_two_elimination_max_price(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type, price=1000)
        self.home1 = self.create_home(self.home_type, price=1500)
        self.home2 = self.create_home(self.home_type, price=2000)
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.desired_price = 1000
        rent_algorithm.max_price = 1400

        # Set the user scale
        price_user_scale_factor = 1
        rent_algorithm.price_user_scale_factor = price_user_scale_factor
        # Overriding in case the config file changes
        price_question_weight = 100
        rent_algorithm.price_question_weight = price_question_weight

        # Act
        rent_algorithm.run_compute_price_score()

        # Assert

        # Home 0
        self.assertEqual((1 - (0 / 400)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertFalse(rent_algorithm.homes[0].eliminated)

        # Home 1
        self.assertEqual(-100, rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertTrue(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual(-100, rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertTrue(rent_algorithm.homes[2].eliminated)

    def test_run_compute_price_score_working_varied_user_scale_positive(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type, price=1000)
        self.home1 = self.create_home(self.home_type, price=1500)
        self.home2 = self.create_home(self.home_type, price=2000)
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.desired_price = 1000
        rent_algorithm.max_price = 2500

        # Set the user scale
        price_user_scale_factor = 5
        rent_algorithm.price_user_scale_factor = price_user_scale_factor
        # Overriding in case the config file changes
        price_question_weight = 100
        rent_algorithm.price_question_weight = price_question_weight

        # Act
        rent_algorithm.run_compute_price_score()

        # Assert

        # Home 0
        self.assertEqual((1 - (0 / 1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertFalse(rent_algorithm.homes[0].eliminated)

        # Home 1
        self.assertEqual((1 - (500 / 1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual((1 - (1000 / 1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertFalse(rent_algorithm.homes[2].eliminated)


class TestRentAlgorithmJustApproximateCommuteScore(TestCase):

    def setUp(self):
        # Create a commute type
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        HomeProviderModel.objects.create(provider="MLSPIN")
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile=self.user_profile)

        self.home_type = HomeTypeModel.objects.create(home_type='House')

    def create_destination(self, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return self.survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    def test_run_compute_commute_score_approximate_working(self):
        """
        This tests to make sure when given correctly values, everything works properly. Kinda of a sanity check unit
            test
        """
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the destinations
        self.destination = self.create_destination(self.commute_type, min_commute=50, max_commute=110, commute_weight=1)

        self.destination1 = self.create_destination(self.commute_type, min_commute=50, max_commute=90, commute_weight=2)

        self.destination2 = self.create_destination(self.commute_type, min_commute=30, max_commute=110, commute_weight=3)

        # Set the commute times to each destination

        # Home 0
        self.home.approx_commute_times = {self.destination: 50}
        self.home.approx_commute_times = {self.destination1: 70}

        # Home 1
        self.home1.approx_commute_times = {self.destination: 10}
        self.home1.approx_commute_times = {self.destination1: 80}
        self.home1.approx_commute_times = {self.destination2: 100}

        # Home 2
        self.home2.approx_commute_times = {self.destination: 60}

        # Add homes to algorithm
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_approximate()

        # Assert

        # Home 0
        self.assertEqual(((1 - (0 / 60)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (20 / 40)) * self.destination1.commute_weight * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight,
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0 / 60)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (30 / 40)) * self.destination1.commute_weight * commute_question_weight) +
                         ((1 - (70 / 80)) * self.destination2.commute_weight * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight +
                         self.destination2.commute_weight * commute_question_weight,
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (10 / 60)) * self.destination.commute_weight * commute_question_weight),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight,
                         rent_algorithm.homes[2].total_possible_points)

    def test_run_compute_commute_score_approximate_working_large_user_scale_factor(self):
        """
        This unit tests checks that even with large user scale factors, everything works correctly
        """
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the destinations
        self.destination = self.create_destination(self.commute_type, min_commute=0, max_commute=100, commute_weight=5)

        self.destination1 = self.create_destination(self.commute_type, min_commute=10, max_commute=80, commute_weight=6)

        self.destination2 = self.create_destination(self.commute_type, min_commute=7, max_commute=120, commute_weight=5)

        # Set the commute times to each destination

        # Home 0
        self.home.approx_commute_times = {self.destination: 50}
        self.home.approx_commute_times = {self.destination1: 70}

        # Home 1
        self.home1.approx_commute_times = {self.destination: 10}
        self.home1.approx_commute_times = {self.destination1: 80}
        self.home1.approx_commute_times = {self.destination2: 100}

        # Home 2
        self.home2.approx_commute_times = {self.destination: 60}

        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_approximate()

        # Assert

        # Home 0
        self.assertEqual(((1 - (50 / 100)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (60 / 70)) * self.destination1.commute_weight * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight,
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (10 / 100)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (70 / 70)) * self.destination1.commute_weight * commute_question_weight) +
                         ((1 - (93 / 113)) * self.destination2.commute_weight * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight +
                         self.destination2.commute_weight * commute_question_weight,
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (60 / 100)) * self.destination.commute_weight * commute_question_weight),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight,
                         rent_algorithm.homes[2].total_possible_points)


class TestRentAlgorithmJustExactCommuteScore(TestCase):

    def setUp(self):
        # Create a commute type
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        HomeProviderModel.objects.create(provider="MLSPIN")

        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile=self.user_profile)

        # Start creating the homes
        self.home_type = HomeTypeModel.objects.create(home_type='House')

    def create_destination(self, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return self.survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    def test_run_compute_commute_score_exact_working(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the destinations
        self.destination = self.create_destination(self.commute_type, min_commute=3, max_commute=76, commute_weight=1)

        self.destination1 = self.create_destination(self.commute_type, min_commute=50, max_commute=110, commute_weight=2)

        self.destination2 = self.create_destination(self.commute_type, min_commute=10, max_commute=120, commute_weight=0)

        # Home 0
        self.home.exact_commute_times = {self.destination: 50}
        self.home.exact_commute_times = {self.destination1: 70}

        # Home 1
        self.home1.exact_commute_times = {self.destination: 10}
        self.home1.exact_commute_times = {self.destination1: 80}
        self.home1.exact_commute_times = {self.destination2: 100}

        # Home 2
        self.home2.exact_commute_times = {self.destination: 60}

        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_exact()

        # Assert

        # Home 0
        self.assertEqual(((1 - (47 / 73)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (20 / 60)) * self.destination1.commute_weight * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight,
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (7 / 73)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (30 / 60)) * self.destination1.commute_weight * commute_question_weight) +
                         ((1 - (90 / 110)) * self.destination2.commute_weight * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight +
                         self.destination2.commute_weight * commute_question_weight,
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (57 / 73)) * self.destination.commute_weight * commute_question_weight),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight,
                         rent_algorithm.homes[2].total_possible_points)

    def test_run_compute_commute_score_exact_working_large_user_scale_factor(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)

        # Create the destinations
        self.destination = self.create_destination(self.commute_type, min_commute=30, max_commute=100, commute_weight=5)

        self.destination1 = self.create_destination(self.commute_type, min_commute=20, max_commute=90, commute_weight=6)

        self.destination2 = self.create_destination(self.commute_type, min_commute=10, max_commute=180, commute_weight=5)

        # Home 0
        self.home.exact_commute_times = {self.destination: 50}
        self.home.exact_commute_times = {self.destination1: 70}

        # Home 1
        self.home1.exact_commute_times = {self.destination: 10}
        self.home1.exact_commute_times = {self.destination1: 80}
        self.home1.exact_commute_times = {self.destination2: 100}

        # Home 2
        self.home2.exact_commute_times = {self.destination: 60}

        # Add homes to algorithm
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_exact()

        # Assert

        # Home 0
        self.assertEqual(((1 - (20 / 70)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (50 / 70)) * self.destination1.commute_weight * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight,
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0 / 70)) * self.destination.commute_weight * commute_question_weight) +
                         ((1 - (60 / 70)) * self.destination1.commute_weight * commute_question_weight) +
                         ((1 - (90 / 170)) * self.destination2.commute_weight * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight +
                         self.destination1.commute_weight * commute_question_weight +
                         self.destination2.commute_weight * commute_question_weight,
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (30 / 70)) * self.destination.commute_weight * commute_question_weight),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(self.destination.commute_weight * commute_question_weight,
                         rent_algorithm.homes[2].total_possible_points)


class TestRentAlgorithmJustSortHomeByScore(TestCase):

    def setUp(self):
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        HomeProviderModel.objects.create(provider="MLSPIN")
        self.home_type = HomeTypeModel.objects.create(home_type='House')

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    def test_run_sort_home_by_score(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)
        # Home 0
        rent_algorithm.homes = self.home
        rent_algorithm.homes[0].accumulated_points = 60
        rent_algorithm.homes[0].total_possible_points = 120
        # Home 1
        rent_algorithm.homes = self.home1
        rent_algorithm.homes[1].accumulated_points = 70
        rent_algorithm.homes[1].total_possible_points = 120
        # Home 2
        rent_algorithm.homes = self.home2
        rent_algorithm.homes[2].accumulated_points = 50
        rent_algorithm.homes[2].total_possible_points = 120

        # Act
        rent_algorithm.run_sort_home_by_score()

        # Assert
        self.assertEqual(self.home, rent_algorithm.homes[1])
        self.assertEqual(self.home1, rent_algorithm.homes[0])
        self.assertEqual(self.home2, rent_algorithm.homes[2])

    def test_run_sort_home_by_score_homes_equal_different_total_possible_points(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)
        # Home 0
        rent_algorithm.homes = self.home
        rent_algorithm.homes[0].accumulated_points = 60
        rent_algorithm.homes[0].total_possible_points = 120
        # Home 1
        rent_algorithm.homes = self.home1
        rent_algorithm.homes[1].accumulated_points = 120
        rent_algorithm.homes[1].total_possible_points = 240
        # Home 2
        rent_algorithm.homes = self.home2
        rent_algorithm.homes[2].accumulated_points = 240
        rent_algorithm.homes[2].total_possible_points = 480

        # Act
        rent_algorithm.run_sort_home_by_score()

        # Assert
        self.assertEqual(self.home, rent_algorithm.homes[2])
        self.assertEqual(self.home1, rent_algorithm.homes[1])
        self.assertEqual(self.home2, rent_algorithm.homes[0])

    def test_run_sort_home_by_score_some_negative(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        self.home = self.create_home(self.home_type)
        self.home1 = self.create_home(self.home_type)
        self.home2 = self.create_home(self.home_type)
        # Home 0
        rent_algorithm.homes = self.home
        rent_algorithm.homes[0].accumulated_points = 60
        rent_algorithm.homes[0].total_possible_points = 120
        # Home 1
        rent_algorithm.homes = self.home1
        rent_algorithm.homes[1].accumulated_points = -120
        rent_algorithm.homes[1].total_possible_points = 240
        # Home 2
        rent_algorithm.homes = self.home2
        rent_algorithm.homes[2].accumulated_points = -240
        rent_algorithm.homes[2].total_possible_points = 480

        # Act
        rent_algorithm.run_sort_home_by_score()

        # Assert
        self.assertEqual(self.home, rent_algorithm.homes[0])
        self.assertEqual(self.home1, rent_algorithm.homes[2])
        self.assertEqual(self.home2, rent_algorithm.homes[1])


class TestRentAlgorithmPopulateSurveyDestinationsAndPossibleHomes(TestCase):

    def setUp(self):
        # Create a commute type
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        # Create possible home types
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        self.home_type1 = HomeTypeModel.objects.create(home_type='Apartment')

        # Some house values
        self.price_min = 1000
        self.price_middle = 1500
        self.price_max = 2000
        self.move_in_day_home = timezone.now()
        self.move_in_day_home1 = timezone.now() + timezone.timedelta(days=1)
        self.num_bedrooms_min = 2
        self.num_bedrooms_max = 3
        self.num_bathrooms_min = 2
        self.num_bathrooms_middle = 3
        self.num_bathrooms_max = 4

        # Create a user so the survey form can validate
        self.user = MyUser.objects.create(email="test@email.com")
        HomeProviderModel.objects.create(provider="MLSPIN")

        # Create some destination variables
        self.street_address = "12 Stony Brook Rd"
        self.city = "Arlington"
        self.state = "MA"
        self.zip_code = '02476'

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_destination(survey, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_type=None,
                           commute_weight=0, max_commute=60, min_commute=0):
        if commute_type is None:
            commute_type = CommuteType.objects.get(commute_type=CommuteType.DRIVING)
        return survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    def tests_populate_survey_homes_2_bedrooms(self):
        """
        Verifies that given the survey, one home is successfully returned
        """
        # Arrange
        rent_algorithm = RentAlgorithm()
        # Make some homes
        self.home = self.create_home(self.home_type,
                                     price=self.price_min,
                                     num_bathrooms=self.num_bathrooms_min,
                                     num_bedrooms=self.num_bedrooms_min)
        self.home1 = self.create_home(self.home_type,
                                      price=self.price_middle,
                                      num_bathrooms=self.num_bathrooms_middle,
                                      num_bedrooms=self.num_bedrooms_max)
        self.home2 = self.create_home(self.home_type,
                                      price=self.price_max,
                                      num_bathrooms=self.num_bathrooms_min,
                                      num_bedrooms=self.num_bedrooms_min,
                                      currently_available=False)
        self.home3 = self.create_home(self.home_type,
                                      price=self.price_min,
                                      num_bathrooms=self.num_bathrooms_max,
                                      num_bedrooms=self.num_bedrooms_max,
                                      currently_available=False)
        self.home4 = self.create_home(self.home_type,
                                      price=self.price_max,
                                      num_bathrooms=self.num_bathrooms_min,
                                      num_bedrooms=self.num_bedrooms_min)
        # Create the survey
        survey = self.create_survey(self.user.userProfile)
        survey.home_type.set([self.home_type, self.home_type1])

        # Act
        rent_algorithm.populate_survey_homes(survey)

        # Assert
        self.assertEqual(1, len(rent_algorithm.homes))
        self.assertEqual(self.home.home, rent_algorithm.homes[0].home)

    def tests_populate_survey_homes_2_bedrooms_higher_max_price(self):
        """
        Verifies that given the survey, two homes is successfully returned
        """
        # Arrange
        rent_algorithm = RentAlgorithm()
        # Make some homes
        self.home = self.create_home(self.home_type,
                                     price=self.price_min,
                                     num_bathrooms=self.num_bathrooms_min,
                                     num_bedrooms=self.num_bedrooms_min)
        self.home1 = self.create_home(self.home_type,
                                      price=self.price_middle,
                                      num_bathrooms=self.num_bathrooms_middle,
                                      num_bedrooms=self.num_bedrooms_max)
        self.home2 = self.create_home(self.home_type,
                                      price=self.price_max,
                                      num_bathrooms=self.num_bathrooms_min,
                                      num_bedrooms=self.num_bedrooms_min,
                                      currently_available=False)
        self.home3 = self.create_home(self.home_type,
                                      price=self.price_min,
                                      num_bathrooms=self.num_bathrooms_max,
                                      num_bedrooms=self.num_bedrooms_max,
                                      currently_available=False)
        self.home4 = self.create_home(self.home_type,
                                      price=self.price_max,
                                      num_bathrooms=self.num_bathrooms_min,
                                      num_bedrooms=self.num_bedrooms_min)
        # Create the survey
        survey = self.create_survey(self.user.userProfile, max_price=3000)
        survey.home_type.set([self.home_type, self.home_type1])

        # Act
        rent_algorithm.populate_survey_homes(survey)

        # Assert
        self.assertEqual(2, len(rent_algorithm.homes))
        self.assertEqual(self.home.home, rent_algorithm.homes[0].home)
        self.assertEqual(self.home4.home, rent_algorithm.homes[1].home)


class TestRetrieveApproximateCommutes(TestCase):

    def setUp(self):
        # Create a user so the survey form can validate
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    def test_retrieve_approx_commutes_driving_transit(self):
        """
        This tests that is one home is inputted and one destination with driving or transit and the home is not
        eliminated, then the home is not eliminated
        """
        # Arrange
        commute_type_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_type_driving)

        # Start the algorithm
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [home]
        rent_algorithm.tenants = [destination]
        homes = [home]

        # Mock the functions to just test this one function

        # Tests that the home is valid and is not eliminated
        rent_algorithm.populate_approx_commutes = MagicMock()
        # Doesn't have a return but prevents updating the database unnecessarily
        commute_cache_updater.update_commutes_cache_rent_algorithm = MagicMock()

        # Act
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert
        commute_cache_updater.update_commutes_cache_rent_algorithm.assert_called_once_with(homes, [destination],
                                                                                           accuracy=CommuteAccuracy.APPROXIMATE)
        rent_algorithm.populate_approx_commutes.assert_called_once_with(homes, destination, lat_lng_dest="")

    def test_retrieve_approx_commutes_walking(self):
        """
        This tests that is one home is inputted and one destination with bicycling or waking and the home is not
        eliminated, then the home is not eliminated and the correct lat_lng is generated and passed
        """
        # Arrange
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_type_walking)

        # Start the algorithm
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [home]
        rent_algorithm.tenants = [destination]
        homes = [home]

        # Mock the functions to just test this one function

        # Tests that the home is valid and is not eliminated
        rent_algorithm.populate_approx_commutes = MagicMock(return_value=True)
        # Doesn't have a return but prevents updating the database unnecessarily
        commute_cache_updater.update_commutes_cache_rent_algorithm = MagicMock()
        # Prevent google maps query
        geolocator.maps_requester.get_lat_lon_from_address = MagicMock(return_value=(42.4080528, -71.1632442))

        # Act
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert
        commute_cache_updater.update_commutes_cache_rent_algorithm.assert_called_once_with(homes, [destination],
                                                                                           accuracy=CommuteAccuracy.APPROXIMATE)
        rent_algorithm.populate_approx_commutes.assert_called_once_with(homes, destination,
                                                              lat_lng_dest=(42.4080528, -71.1632442))

    def test_retrieve_approx_commutes_some_dest_driving_some_biking(self):
        """
        Checks to
        """
        # Arrange
        commute_type_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        commute_type_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)
        commute_type_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type)
        home1 = self.create_home(self.home_type)
        home2 = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_type_driving)
        destination1 = self.create_destination(survey, commute_type=commute_type_transit)
        destination2 = self.create_destination(survey, commute_type=commute_type_bicycling)

        # Start the algorithm
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [home, home1, home2]
        rent_algorithm.tenants = [destination, destination1, destination2]
        homes = [home, home1, home2]

        # Mock the functions to just test this one function

        # Tests that the home is valid and is not eliminated
        rent_algorithm.populate_approx_commutes = MagicMock()
        # Doesn't have a return but prevents updating the database unnecessarily
        commute_cache_updater.update_commutes_cache_rent_algorithm = MagicMock()
        # Prevent google maps query
        geolocator.maps_requester.get_lat_lon_from_address = MagicMock(return_value=(42.4080528, -71.1632442))

        # Act
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert
        commute_cache_updater.update_commutes_cache_rent_algorithm.assert_called_once_with(homes,
                                                                                           [destination, destination1, destination2],
                                                                                           accuracy=CommuteAccuracy.APPROXIMATE)
        rent_algorithm.populate_approx_commutes.assert_has_calls(
            [call(homes, destination, lat_lng_dest=""),
             call(homes, destination1, lat_lng_dest=""),
             call(homes, destination2, lat_lng_dest=(42.4080528, -71.1632442))]
        )


class TestApproxCommute(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,

        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2,
                    zip_code="02476", state="MA", latitude=0.0, longitude=0.0):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            latitude=latitude,
            longitude=longitude,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    @staticmethod
    def create_zip_code_dictionary(zip_code):
        return ZipCodeBase.objects.create(zip_code=zip_code)

    @staticmethod
    def create_zip_code_dictionary_child(parent_zip_code_dictionary, zip_code, commute_time,
                                         commute_distance, commute_type, last_updated=timezone.now()):
        parent_zip_code_dictionary.zipcodechild_set.create(
            zip_code=zip_code,
            commute_time_seconds=commute_time,
            commute_distance_meters=commute_distance,
            commute_type=commute_type,
            last_date_updated=last_updated,
        )

    def test_populate_approx_commute_times_driving(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type)

        rent_algorithm = RentAlgorithm()
        rent_algorithm.zip_code_approximation = MagicMock()
        rent_algorithm.lat_lng_approximation = MagicMock()

        homes = [home]

        # Act
        rent_algorithm.populate_approx_commutes(homes, destination)

        # Assert
        rent_algorithm.zip_code_approximation.assert_called_once_with(homes, destination)
        rent_algorithm.lat_lng_approximation.assert_not_called()

    def test_populate_approx_commute_times_transit(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        commute_type_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)
        destination = self.create_destination(survey, commute_type_transit)

        rent_algorithm = RentAlgorithm()
        rent_algorithm.zip_code_approximation = MagicMock()
        rent_algorithm.lat_lng_approximation = MagicMock()

        homes = [home]

        # Act
        rent_algorithm.populate_approx_commutes(homes, destination)

        # Assert
        rent_algorithm.zip_code_approximation.assert_called_once_with(homes, destination)
        rent_algorithm.lat_lng_approximation.assert_not_called()

    def test_populate_approx_commute_times_bicycling(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        commute_type_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        destination = self.create_destination(survey, commute_type_bicycling)
        latlng = (5, 10)

        rent_algorithm = RentAlgorithm()
        rent_algorithm.zip_code_approximation = MagicMock()
        rent_algorithm.lat_lng_approximation = MagicMock()

        homes = [home]

        # Act
        rent_algorithm.populate_approx_commutes(homes, destination, lat_lng_dest=latlng)

        # Assert
        rent_algorithm.zip_code_approximation.assert_not_called()
        rent_algorithm.lat_lng_approximation.assert_called_once_with(homes, destination, latlng, AVERAGE_BICYCLING_SPEED)

    def test_populate_approx_commute_times_walking(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        destination = self.create_destination(survey, commute_type_walking)
        latlng = (5, 10)

        rent_algorithm = RentAlgorithm()
        rent_algorithm.zip_code_approximation = MagicMock()
        rent_algorithm.lat_lng_approximation = MagicMock()

        homes = [home]

        # Act
        rent_algorithm.populate_approx_commutes(homes, destination, lat_lng_dest=latlng)

        # Assert
        rent_algorithm.zip_code_approximation.assert_not_called()
        rent_algorithm.lat_lng_approximation.assert_called_once_with(homes, destination, latlng, AVERAGE_WALKING_SPEED)

    def test_zip_code_approximation_combo_exists(self):
        """
        Tests that if the zip_combo exists then it will extract it from the zip-code database and use the values
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="100 Main Street")
        zip_code = '02476'
        home = self.create_home(self.home_type, zip_code=zip_code)
        home1 = self.create_home(self.home_type, zip_code='02474')
        commute_distance = 100
        commute_time_seconds = 376

        homes = [home, home1]

        # Create the zip-code dictionary
        parent_zip_code = self.create_zip_code_dictionary(destination.zip_code)
        self.create_zip_code_dictionary_child(parent_zip_code, zip_code, commute_time_seconds,
                                              commute_distance, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code, '02474', commute_time_seconds,
                                              commute_distance, self.commute_type)

        # Act
        RentAlgorithm.zip_code_approximation(homes, destination)

        # Assert
        # Convert to minutes because that is what is returned
        self.assertEqual(home.approx_commute_times, {destination: commute_time_seconds / 60})
        self.assertEqual(home1.approx_commute_times, {destination: commute_time_seconds / 60})

    def test_zip_code_approximation_child_does_not_exist(self):
        """
        Tests that if the parent zip code exists but not the child, then the function will return false
            and the home will not be added to the list of commute times
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="100 Main Street")
        zip_code = '02476'
        home = self.create_home(self.home_type)
        home1 = self.create_home(self.home_type)
        homes = [home, home1]

        # Create the zip-code dictionary
        self.create_zip_code_dictionary(zip_code)

        # Act
        RentAlgorithm.zip_code_approximation(homes, destination)

        # Assert
        # Convert to minutes because that is what is returned
        self.assertEqual(home.approx_commute_times, {})
        self.assertEqual(home1.approx_commute_times, {})

    def test_zip_code_approximation_neither_exist(self):
        """
        Tests that if the parent/child zip code approximation doesn't exist then the function will return false and
            the commute is not added to the approx_commute_times
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="100 Main Street")
        zip_code = '02476'
        home = self.create_home(self.home_type)
        homes = [home]

        # Act
        RentAlgorithm.zip_code_approximation(homes, destination)

        # Assert
        # Convert to minutes because that is what is returned
        self.assertEqual(home.approx_commute_times, {})

    def test_lat_lng_approximation_bicycling(self):
        """
        Tests that the lat_lng approximation for for bicycling
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type, latitude=42.399305, longitude=-71.135242)
        commute_type_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        destination = self.create_destination(survey, commute_type_bicycling)
        homes = [home]

        # Act
        RentAlgorithm.lat_lng_approximation(homes, destination, (42.4080528, -71.1632442),
                                            average_speed=AVERAGE_BICYCLING_SPEED)

        # Assert
        self.assertAlmostEqual(home.approx_commute_times[destination], 17.8878, places=3)

    def test_lat_lng_approximation_walking(self):
        """
        Tests that the lat lng approximation works for walking
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type, latitude=42.399305, longitude=-71.135242)
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        destination = self.create_destination(survey, commute_type_walking)
        homes = [home]

        # Act
        RentAlgorithm.lat_lng_approximation(homes, destination, (42.4080528, -71.1632442),
                                            average_speed=AVERAGE_WALKING_SPEED)

        # Assert
        self.assertAlmostEqual(home.approx_commute_times[destination], 39.6506, places=3)

    def test_lat_lng_approximation_walking_multiple_homes(self):
        """
        Tests that the lat lng approximation works for walking with multiple homes
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type, latitude=42.399305, longitude=-71.135242)
        home1 = self.create_home(self.home_type, latitude=42.36, longitude=-71.2)
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        destination = self.create_destination(survey, commute_type_walking)
        homes = [home, home1]

        # Act
        RentAlgorithm.lat_lng_approximation(homes, destination, (42.4080528, -71.1632442),
                                            average_speed=AVERAGE_WALKING_SPEED)

        # Assert
        self.assertAlmostEqual(home.approx_commute_times[destination], 39.6506, places=3)
        self.assertAlmostEqual(home1.approx_commute_times[destination], 93.9631, places=3)

    def test_lat_lng_approximation_average_speed_zero(self):
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type, latitude=42.408021, longitude=-71.163222)
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        destination = self.create_destination(survey, commute_type_walking)
        homes = [home]

        # Act
        RentAlgorithm.lat_lng_approximation(homes, destination, (42.415656, -71.165393),
                                            average_speed=0)

        # Assert
        self.assertEqual(home.approx_commute_times, {})


# TODO fix exact commutes to use mocking
class TestRetrieveExactCommutes(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA",
                    street_address="12 Stony Brook Rd", city="Arlington"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            street_address=street_address,
            city=city,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    @skip("Renable when mocked")
    def test_retrieve_exact_commute_simple_case(self):
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="159 Brattle Street",
                                              city="Arlington", state="MA", zip_code="02474")

        house = self.create_home(self.home_type, zip_code="02052", city="Medfield", state="MA",
                                 street_address="2 Snow Hill Lane")

        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [house]
        rent_algorithm.tenants = [destination]

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].exact_commute_times,
                         {destination: 39})

    @skip('Calls api')
    def test_retrieve_exact_commute_zero_origin(self):
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="159 Brattle Street",
                                              city="Arlington", state="MA", zip_code="02474")
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = []
        rent_algorithm.tenants = [destination]

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(len(rent_algorithm.homes), 0)

    @skip('calls api')
    def test_retrieve_exact_commute_no_destinations(self):
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        house = self.create_home(self.home_type, zip_code="02052", city="Medfield", state="MA",
                                 street_address="2 Snow Hill Lane")
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [house]
        rent_algorithm.tenants = []

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].exact_commute_times, {})

    @skip("reenable when distance matrix is mocked")
    def test_retrieve_exact_commute_multiple_origins(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [self.home, self.home2]
        destination1 = self.create_destination("350 Prospect Street",
                                               "Belmont",
                                               "MA",
                                               "02478")
        rent_algorithm.tenants = [destination1]

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].exact_commute_times,
                         {"350 Prospect Street-Belmont-MA-02478": 32})
        self.assertEqual(rent_algorithm.homes[1].exact_commute_times,
                         {"350 Prospect Street-Belmont-MA-02478": 8})

# TODO: stress test the algorithm with a mock API and the MLS data