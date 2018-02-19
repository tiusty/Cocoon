from django.test import TestCase
from django.utils import timezone

# Import external models
from houseDatabase.models import RentDatabaseModel, HomeTypeModel, ZipCodeDictionaryParentModel, CommuteTypeModel, MlsManagementModel
# Import survey python modules
from survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from survey.home_data.home_score import HomeScore
from survey.models import RentingSurveyModel, RentingDestinationsModel
from userAuth.models import MyUser, UserProfile


# Import DistanceWrapper


class TestRentAlgorithmJustApproximateCommuteFilter(TestCase):

    def setUp(self):
        # Create a commute type
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='Driving')
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile_survey=self.user_profile,
                                                        commute_type_survey=self.commute_type)

        # Add renting destination
        self.street_address = '12 Stony Brook Rd'
        self.city = 'Arlington'
        self.state = 'MA'
        self.zip_code = '02476'
        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address,
            city_destination=self.city,
            state_destination=self.state,
            zip_code_destination=self.zip_code
        )

        self.street_address1 = '8 Stony Brook Rd'
        self.city1 = 'Arlington'
        self.state1 = 'MA'
        self.zip_code1 = '02476'
        self.destination1 = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address1,
            city_destination=self.city1,
            state_destination=self.state1,
            zip_code_destination=self.zip_code1
        )

        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home.approx_commute_times = {self.destination.destination_key: 50}
        self.home.approx_commute_times = {self.destination1.destination_key: 70}
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1.approx_commute_times = {self.destination.destination_key: 10}
        self.home1.approx_commute_times = {self.destination1.destination_key: 70}
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2.approx_commute_times = {self.destination.destination_key: 40}
        self.home2.approx_commute_times = {self.destination1.destination_key: 100}

    def test_run_compute_approximate_commute_filter_no_eliminations(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_user_commute = 30
        rent_algorithm.max_user_commute = 80
        rent_algorithm.approx_commute_range = 20

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertFalse(rent_algorithm.homes[0].eliminated)
        self.assertFalse(rent_algorithm.homes[1].eliminated)
        self.assertFalse(rent_algorithm.homes[2].eliminated)

    def test_run_compute_approximate_commute_filter_one_elimination(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_user_commute = 10
        rent_algorithm.max_user_commute = 80
        rent_algorithm.approx_commute_range = 10

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertFalse(rent_algorithm.homes[0].eliminated)
        self.assertFalse(rent_algorithm.homes[1].eliminated)
        self.assertTrue(rent_algorithm.homes[2].eliminated)

    def test_run_compute_approximate_commute_filter_all_eliminated(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_user_commute = 60
        rent_algorithm.max_user_commute = 60
        rent_algorithm.approx_commute_range = 0

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertTrue(rent_algorithm.homes[0].eliminated)
        self.assertTrue(rent_algorithm.homes[1].eliminated)
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
        CommuteTypeModel.objects.create(commute_type_field='Driving')
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(price_home=1000, home_type_home=self.home_type))
        self.home1 = HomeScore(RentDatabaseModel.objects.create(price_home=1500, home_type_home=self.home_type))
        self.home2 = HomeScore(RentDatabaseModel.objects.create(price_home=2000, home_type_home=self.home_type))

    def test_run_compute_price_score_working(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1000
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

    def test_run_compute_price_score_one_elimination_min_price(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1100
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
        self.assertEqual((1 - (400 / 1400)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual((1 - (900 / 1400)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertFalse(rent_algorithm.homes[2].eliminated)

    def test_run_compute_price_score_two_eliminations_min_price(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1600
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
        self.assertEqual((1 - (400 / 900)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertFalse(rent_algorithm.homes[2].eliminated)

    def test_run_compute_price_score_one_elimination_max_price(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1000
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
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1000
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
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_price = 1000
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
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='Driving')
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile_survey=self.user_profile,
                                                        commute_type_survey=self.commute_type)

        # Add renting destination
        self.street_address = '12 Stony Brook Rd'
        self.city = 'Arlington'
        self.state = 'MA'
        self.zip_code = '02476'
        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address,
            city_destination=self.city,
            state_destination=self.state,
            zip_code_destination=self.zip_code
        )

        self.street_address1 = '8 Stony Brook Rd'
        self.city1 = 'Arlington'
        self.state1 = 'MA'
        self.zip_code1 = '02476'
        self.destination1 = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address1,
            city_destination=self.city1,
            state_destination=self.state1,
            zip_code_destination=self.zip_code1
        )

        self.street_address2 = '360 Huntington Ave'
        self.city2 = 'Boston'
        self.state2 = 'MA'
        self.zip_code2 = '02115'
        self.destination2 = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address2,
            city_destination=self.city2,
            state_destination=self.state2,
            zip_code_destination=self.zip_code2
        )

        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home.approx_commute_times = {self.destination.destination_key: 50}
        self.home.approx_commute_times = {self.destination1.destination_key: 70}
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1.approx_commute_times = {self.destination.destination_key: 10}
        self.home1.approx_commute_times = {self.destination1.destination_key: 80}
        self.home1.approx_commute_times = {self.destination2.destination_key: 100}
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2.approx_commute_times = {self.destination.destination_key: 60}

    def test_run_compute_commute_score_approximate_working(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_user_commute = 50
        rent_algorithm.max_user_commute = 110

        # Set user scale factor
        commute_user_scale_factor = 1
        rent_algorithm.commute_user_scale_factor = commute_user_scale_factor

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_approximate()

        # Assert

        # Home 0
        self.assertEqual(((1 - (0 / 60)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (20 / 60)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[0].approx_commute_times) * (commute_question_weight
                                                                              * commute_user_scale_factor),
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0 / 60)) * commute_question_weight * commute_user_scale_factor)
                         + ((1 - (30 / 60)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (50 / 60)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[1].approx_commute_times) * (commute_question_weight
                                                                              * commute_user_scale_factor),
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (10 / 60)) * commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[2].approx_commute_times) * (commute_question_weight
                                                                              * commute_user_scale_factor),
                         rent_algorithm.homes[2].total_possible_points)

    def test_run_compute_commute_score_approximate_working_large_user_scale_factor(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_user_commute = 30
        rent_algorithm.max_user_commute = 100

        # Set user scale factor
        commute_user_scale_factor = 5
        rent_algorithm.commute_user_scale_factor = commute_user_scale_factor

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_approximate()

        # Assert

        # Home 0
        self.assertEqual(((1 - (20 / 70)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (40 / 70)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[0].approx_commute_times) * (commute_question_weight
                                                                              * commute_user_scale_factor),
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0 / 70)) * commute_question_weight * commute_user_scale_factor)
                         + ((1 - (50 / 70)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (70 / 70)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[1].approx_commute_times) * (commute_question_weight
                                                                              * commute_user_scale_factor),
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (30 / 70)) * commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[2].approx_commute_times) * (commute_question_weight
                                                                              * commute_user_scale_factor),
                         rent_algorithm.homes[2].total_possible_points)


class TestRentAlgorithmJustExactCommuteScore(TestCase):

    def setUp(self):
        # Create a commute type
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='Driving')
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile_survey=self.user_profile,
                                                        commute_type_survey=self.commute_type)

        # Add renting destination
        self.street_address = '12 Stony Brook Rd'
        self.city = 'Arlington'
        self.state = 'MA'
        self.zip_code = '02476'
        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address,
            city_destination=self.city,
            state_destination=self.state,
            zip_code_destination=self.zip_code
        )

        self.street_address1 = '8 Stony Brook Rd'
        self.city1 = 'Arlington'
        self.state1 = 'MA'
        self.zip_code1 = '02476'
        self.destination1 = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address1,
            city_destination=self.city1,
            state_destination=self.state1,
            zip_code_destination=self.zip_code1
        )

        self.street_address2 = '360 Huntington Ave'
        self.city2 = 'Boston'
        self.state2 = 'MA'
        self.zip_code2 = '02115'
        self.destination2 = self.survey.rentingdestinationsmodel_set.create(
            street_address_destination=self.street_address2,
            city_destination=self.city2,
            state_destination=self.state2,
            zip_code_destination=self.zip_code2
        )

        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home.exact_commute_times = {self.destination.destination_key: 50}
        self.home.exact_commute_times = {self.destination1.destination_key: 70}
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1.exact_commute_times = {self.destination.destination_key: 10}
        self.home1.exact_commute_times = {self.destination1.destination_key: 80}
        self.home1.exact_commute_times = {self.destination2.destination_key: 100}
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2.exact_commute_times = {self.destination.destination_key: 60}

    def test_run_compute_commute_score_exact_working(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_user_commute = 50
        rent_algorithm.max_user_commute = 110

        # Set user scale factor
        commute_user_scale_factor = 1
        rent_algorithm.commute_user_scale_factor = commute_user_scale_factor

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_exact()

        # Assert

        # Home 0
        self.assertEqual(((1 - (0 / 60)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (20 / 60)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[0].exact_commute_times) * (commute_question_weight
                                                                             * commute_user_scale_factor),
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0 / 60)) * commute_question_weight * commute_user_scale_factor)
                         + ((1 - (30 / 60)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (50 / 60)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[1].exact_commute_times) * (commute_question_weight
                                                                             * commute_user_scale_factor),
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (10 / 60)) * commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[2].exact_commute_times) * (commute_question_weight
                                                                             * commute_user_scale_factor),
                         rent_algorithm.homes[2].total_possible_points)

    def test_run_compute_commute_score_exact_working_large_user_scale_factor(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = self.home
        rent_algorithm.homes = self.home1
        rent_algorithm.homes = self.home2
        rent_algorithm.min_user_commute = 30
        rent_algorithm.max_user_commute = 100

        # Set user scale factor
        commute_user_scale_factor = 5
        rent_algorithm.commute_user_scale_factor = commute_user_scale_factor

        # Overriding in case the config file changes
        commute_question_weight = 100
        rent_algorithm.price_question_weight = commute_question_weight

        # Act
        rent_algorithm.run_compute_commute_score_exact()

        # Assert

        # Home 0
        self.assertEqual(((1 - (20 / 70)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (40 / 70)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[0].exact_commute_times) * (commute_question_weight
                                                                             * commute_user_scale_factor),
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0 / 70)) * commute_question_weight * commute_user_scale_factor)
                         + ((1 - (50 / 70)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (70 / 70)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[1].exact_commute_times) * (commute_question_weight
                                                                             * commute_user_scale_factor),
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (30 / 70)) * commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[2].exact_commute_times) * (commute_question_weight
                                                                             * commute_user_scale_factor),
                         rent_algorithm.homes[2].total_possible_points)


class TestRentAlgorithmJustSortHomeByScore(TestCase):

    def setUp(self):
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='Driving')
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))

    def test_run_sort_home_by_score(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
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
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='Driving')
        # Create possible home types
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home_type1 = HomeTypeModel.objects.create(home_type_survey='Apartment')

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

        # Survey values
        self.move_in_day_start = timezone.now()
        self.move_in_day_start1 = timezone.now() + timezone.timedelta(days=1)
        self.move_in_day_end = timezone.now()
        self.move_in_day_end1 = timezone.now() + timezone.timedelta(days=1)
        self.max_bathrooms = 2
        self.max_bathrooms1 = 3
        self.min_bathrooms = 2
        self.min_bathrooms1 = 3

        # Make some homes
        self.home = RentDatabaseModel.objects.create(home_type_home=self.home_type,
                                                     price_home=self.price_min,
                                                     currently_available_home=True,
                                                     num_bathrooms_home=self.num_bathrooms_min,
                                                     num_bedrooms_home=self.num_bedrooms_min)

        self.home1 = RentDatabaseModel.objects.create(home_type_home=self.home_type,
                                                      price_home=self.price_middle,
                                                      currently_available_home=True,
                                                      num_bathrooms_home=self.num_bathrooms_middle,
                                                      num_bedrooms_home=self.num_bedrooms_max)
        self.home2 = RentDatabaseModel.objects.create(home_type_home=self.home_type1,
                                                      price_home=self.price_max,
                                                      currently_available_home=False,
                                                      num_bathrooms_home=self.num_bathrooms_min,
                                                      num_bedrooms_home=self.num_bedrooms_min)
        self.home3 = RentDatabaseModel.objects.create(home_type_home=self.home_type1,
                                                      price_home=self.price_min,
                                                      currently_available_home=False,
                                                      num_bathrooms_home=self.num_bathrooms_max,
                                                      num_bedrooms_home=self.num_bedrooms_max)

        # Create some destination variables
        self.street_address = "12 Stony Brook Rd"
        self.city = "Arlington"
        self.state = "MA"
        self.zip_code = '02476'

        MlsManagementModel.objects.create()

    def tests_populate_survey_destinations_and_possible_homes_query_all_2_bedrooms_with_destination(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        # Create the survey
        survey = RentingSurveyModel.objects.create(
                                                   user_profile_survey=self.user.userProfile,
                                                   max_price_survey=self.price_max,
                                                   min_price_survey=self.price_min,
                                                   max_bathrooms_survey=self.max_bathrooms,
                                                   min_bathrooms_survey=self.min_bathrooms,
                                                   num_bedrooms_survey=self.num_bedrooms_min,
                                                   commute_type_survey=self.commute_type)
        survey.home_type_survey.set([self.home_type, self.home_type1])
        # Create a destination for the survey
        survey.rentingdestinationsmodel_set.create(street_address_destination=self.street_address,
                                                   city_destination=self.city,
                                                   state_destination=self.state,
                                                   zip_code_destination=self.zip_code)

        # Act
        rent_algorithm.populate_survey_destinations_and_possible_homes(survey)

        # Assert
        self.assertEqual(1, len(rent_algorithm.homes))
        self.assertEqual(1, len(rent_algorithm.destinations))
        self.assertEqual(self.home, rent_algorithm.homes[0].home)


class TestRetrieveApproximateCommutes(TestCase):

    def setUp(self):
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.zip_code = "04469" # Orono, ME zipcode
        self.zip_code1 = "04401" # Bangor, ME zipcode
        self.zip_code2 = "04240" # Lewiston, ME zipcode
        self.commute_time = 6000
        self.commute_distance = 700
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='Driving')
        self.home.home.zip_code_home = self.zip_code
        self.home1.home.zip_code_home = self.zip_code1
        self.home2.home.zip_code_home = self.zip_code2
        self.home.home.state_home = "Maine"
        self.home1.home.state_home = "Maine"
        self.home2.home.state_home = "Maine"

    @staticmethod
    def create_zip_code_dictionary(zip_code):
        return ZipCodeDictionaryParentModel.objects.create(zip_code_parent=zip_code)

    @staticmethod
    def create_zip_code_dictionary_child(parent_zip_code_dictionary, zip_code, commute_time,
                                         commute_distance, commute_type):
        parent_zip_code_dictionary.zipcodedictionarychildmodel_set.create(
            zip_code_child=zip_code,
            commute_time_seconds_child=commute_time,
            commute_distance_meters_child=commute_distance,
            commute_type_child=commute_type,
        )

    @staticmethod
    def create_destination(address, city, state, zip):
        return RentingDestinationsModel.objects.create(
            survey_destinations_id="0",
            street_address_destination=address,
            city_destination=city,
            state_destination=state,
            zip_code_destination=zip
        )

    def test_retrieve_approx_commutes_in_database_one_home_one_destination(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [self.home]
        destination = self.create_destination("100 Main Street", "Anytown", "Anystate", "00000")
        rent_algorithm.destinations = [destination]
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)
        self.create_zip_code_dictionary_child(parent_zip_code, "00000", 6000.0, 100.0, self.commute_type)

        # Act
        self.assertEqual(rent_algorithm.homes[0].approx_commute_times, {})
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].approx_commute_times, {"100 Main Street-Anytown-Anystate-00000" : 100.0})

    def test_retrieve_approx_commutes_in_database_several_homes_several_destinations(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [self.home, self.home1, self.home2]
        destination1 = self.create_destination("100 Main Street", "Anytown", "Anystate", "00000")
        destination2 = self.create_destination("200 Center Street", "Anyville", "Anystate", "12345")
        destination3 = self.create_destination("100 Franklin Street", "Somewhere", "Anystate", "23456")
        rent_algorithm.destinations = [destination1, destination2, destination3]

        parent_zip_code1 = self.create_zip_code_dictionary(self.zip_code)
        self.create_zip_code_dictionary_child(parent_zip_code1, "00000", 6000.0, 100.0, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code1, "12345", 3000.0, 100.0, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code1, "23456", 12000.0, 100.0, self.commute_type)

        parent_zip_code2 = self.create_zip_code_dictionary(self.zip_code1)
        self.create_zip_code_dictionary_child(parent_zip_code2, "00000", 1500.0, 100.0, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code2, "12345", 6000.0, 100.0, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code2, "23456", 18000.0, 100.0, self.commute_type)

        parent_zip_code3 = self.create_zip_code_dictionary(self.zip_code2)
        self.create_zip_code_dictionary_child(parent_zip_code3, "00000", 3000.0, 100.0, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code3, "12345", 12000.0, 100.0, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code3, "23456", 6000.0, 100.0, self.commute_type)

        # Act
        for home in rent_algorithm.homes:
            self.assertEqual(home.approx_commute_times, {})
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].approx_commute_times,
                         {"100 Main Street-Anytown-Anystate-00000": 100.0,
                          "200 Center Street-Anyville-Anystate-12345": 50.0,
                          "100 Franklin Street-Somewhere-Anystate-23456": 200.0})
        self.assertEqual(rent_algorithm.homes[1].approx_commute_times,
                         {"100 Main Street-Anytown-Anystate-00000": 25.0,
                          "200 Center Street-Anyville-Anystate-12345": 100.0,
                          "100 Franklin Street-Somewhere-Anystate-23456": 300.0})
        self.assertEqual(rent_algorithm.homes[2].approx_commute_times,
                         {"100 Main Street-Anytown-Anystate-00000": 50.0,
                          "200 Center Street-Anyville-Anystate-12345": 200.0,
                          "100 Franklin Street-Somewhere-Anystate-23456": 100.0})

    def test_retrieve_approx_commutes_not_in_database_no_parent_zip(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.commute_type_query = self.commute_type
        rent_algorithm.homes = [self.home]
        destination = self.create_destination("300 Fern Street", "Bangor", "ME", "04401")
        rent_algorithm.destinations = [destination]

        # Act
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert (These times are place holders, since I don't know what the commute times will be)
        self.assertEqual(self.home.approx_commute_times, {"300 Fern Street-Bangor-ME-04401" : 26.416666666666668})

    def test_retrieve_approx_commutes_not_in_database_with_parent_zip(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.commute_type_query = self.commute_type
        rent_algorithm.homes = [self.home]
        destination = self.create_destination("300 Fern Street", "Bangor", "ME", "04401")
        rent_algorithm.destinations = [destination]
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)

        # Act
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert (These times are place holders, since I don't know what the commute times will be)
        self.assertEqual(self.home.approx_commute_times, {"300 Fern Street-Bangor-ME-04401" : 26.416666666666668})

    def test_retrieve_approx_commutes_not_in_database_many_homes_many_destinations(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.commute_type_query = self.commute_type
        rent_algorithm.homes = [self.home, self.home1, self.home2]
        destination1 = self.create_destination("", "Beverly Hills", "CA", "90210")
        destination2 = self.create_destination("", "Boston", "MA", "02101")
        destination3 = self.create_destination("", "Providence", "RI", "02860")
        rent_algorithm.destinations = [destination1, destination2, destination3]

        # Act
        for home in rent_algorithm.homes:
            self.assertEqual(home.approx_commute_times, {})
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert (These times are place holders, since I don't know what the commute times will be)
        self.assertEqual(rent_algorithm.homes[0].approx_commute_times,
                         {"-Beverly Hills-CA-90210": 2816.5833333333335,
                          "-Boston-MA-02101": 230.53333333333333,
                          "-Providence-RI-02860": 270.46666666666664})
        self.assertEqual(rent_algorithm.homes[1].approx_commute_times,
                         {"-Beverly Hills-CA-90210": 2806.45,
                          "-Boston-MA-02101": 220.4,
                          "-Providence-RI-02860": 260.3333333333333})
        self.assertEqual(rent_algorithm.homes[2].approx_commute_times,
                         {"-Beverly Hills-CA-90210": 2720.983333333333,
                          "-Boston-MA-02101": 134.93333333333334,
                          "-Providence-RI-02860": 174.86666666666667})

    def test_retrieve_approx_commutes_mixed(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.commute_type_query = self.commute_type
        rent_algorithm.homes = [self.home, self.home1, self.home2]
        destination1 = self.create_destination("", "Beverly Hills", "CA", "90210")
        destination2 = self.create_destination("", "Boston", "MA", "02101")
        destination3 = self.create_destination("", "Providence", "RI", "02860")
        rent_algorithm.destinations = [destination1, destination2, destination3]

        # Only a few zip codes and destinations will be in the database
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)
        parent_zip_code1 = self.create_zip_code_dictionary(self.zip_code1)
        self.create_zip_code_dictionary_child(parent_zip_code, "90210", 6000.0, 100.0, self.commute_type)
        self.create_zip_code_dictionary_child(parent_zip_code1, "02101", 18000.0, 100.0, self.commute_type)


        # Act
        for home in rent_algorithm.homes:
            self.assertEqual(home.approx_commute_times, {})
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert (These times are place holders, since I don't know what the commute times will be)
        self.assertEqual(rent_algorithm.homes[0].approx_commute_times,
                         {"-Beverly Hills-CA-90210": 100.0,
                          "-Boston-MA-02101": 230.53333333333333,
                          "-Providence-RI-02860": 270.46666666666664})
        self.assertEqual(rent_algorithm.homes[1].approx_commute_times,
                         {"-Beverly Hills-CA-90210": 2806.45,
                          "-Boston-MA-02101": 300.0,
                          "-Providence-RI-02860": 260.3333333333333})
        self.assertEqual(rent_algorithm.homes[2].approx_commute_times,
                         {"-Beverly Hills-CA-90210": 2720.983333333333,
                          "-Boston-MA-02101": 134.93333333333334,
                          "-Providence-RI-02860": 174.86666666666667})

    def test_retrieve_approx_commutes_edge_case_empty_homes(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.commute_type = "driving"
        rent_algorithm.homes = []
        destination = self.create_destination("", "Beverly Hills", "CA", "90210")
        rent_algorithm.destinations = [destination]

        # Act
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes, [])

    def test_retrieve_approx_commutes_edge_case_empty_destinations(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.commute_type = "driving"
        rent_algorithm.homes = [self.home]
        rent_algorithm.destinations = []

        # Act
        rent_algorithm.retrieve_all_approximate_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].approx_commute_times, {})

    #TODO: Write tests for exact commute computation

class TestRetrieveExactCommutes(TestCase):

    def setUp(self):
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='Driving')
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')

        # setting up full home
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home.home.zip_code_home = "02052"
        self.home.home.city_home = "Medfield"
        self.home.home.state_home = "MA"
        self.home.home.street_address_home = "2 Snow Hill Lane"

        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2.home.zip_code_home = "02474"
        self.home2.home.city_home = "Arlington"
        self.home2.home.state_home = "MA"
        self.home2.home.street_address_home = "159 Brattle Street"

    @staticmethod
    def create_destination(address, city, state, zip):
        return RentingDestinationsModel.objects.create(
            survey_destinations_id="0",
            street_address_destination=address,
            city_destination=city,
            state_destination=state,
            zip_code_destination=zip
        )

    def test_retrieve_exact_commute_simple_case(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [self.home]
        destination1 = self.create_destination("159 Brattle Street",
                                                "Arlington",
                                                "MA",
                                                "02474")
        rent_algorithm.destinations = [destination1]

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].exact_commute_times,
                         {"159 Brattle Street-Arlington-MA-02474": 38})
        
    def test_retrieve_exact_commute_zero_origin(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = []
        destination1 = self.create_destination("159 Brattle Street",
                                                "Arlington",
                                                "MA",
                                                "02474")
        rent_algorithm.destinations = [destination1]

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(len(rent_algorithm.homes), 0)

    def test_retrieve_exact_commute_no_destinations(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [self.home]
        rent_algorithm.destinations = []

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].exact_commute_times, {})

    def test_retrieve_exact_commute_multiple_origins(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        rent_algorithm.homes = [self.home, self.home2]
        destination1 = self.create_destination("350 Prospect Street",
                                               "Belmont",
                                               "MA",
                                               "02478")
        rent_algorithm.destinations = [destination1]

        # Act
        rent_algorithm.retrieve_exact_commutes()

        # Assert
        self.assertEqual(rent_algorithm.homes[0].exact_commute_times,
                         {"350 Prospect Street-Belmont-MA-02478": 32})
        self.assertEqual(rent_algorithm.homes[1].exact_commute_times,
                         {"350 Prospect Street-Belmont-MA-02478": 8})

# TODO: stress test the algorithm with a mock API and the MLS data