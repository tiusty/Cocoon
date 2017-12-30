from django.test import TestCase
from django.utils import timezone

# Import survey python modules
from survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from survey.home_data.home_score import HomeScore

# Import external models
from houseDatabase.models import RentDatabaseModel, HomeTypeModel
from survey.models import RentingSurveyModel
from userAuth.models import MyUser, UserProfile


class TestRentAlgorithmJustApproximateCommuteFilter(TestCase):

    def setUp(self):
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home.approx_commute_times = 50
        self.home.approx_commute_times = 70
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1.approx_commute_times = 10
        self.home1.approx_commute_times = 70
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2.approx_commute_times = 40
        self.home2.approx_commute_times = 100

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
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home.approx_commute_times = 50
        self.home.approx_commute_times = 70
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1.approx_commute_times = 10
        self.home1.approx_commute_times = 80
        self.home1.approx_commute_times = 100
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2.approx_commute_times = 60

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
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home.exact_commute_times = 50
        self.home.exact_commute_times = 70
        self.home1 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home1.exact_commute_times = 10
        self.home1.exact_commute_times = 80
        self.home1.exact_commute_times = 100
        self.home2 = HomeScore(RentDatabaseModel.objects.create(home_type_home=self.home_type))
        self.home2.exact_commute_times = 60

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
        self.user_profile = UserProfile.objects.get(user=self.user)

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
                                                     move_in_day_home=self.move_in_day_home,
                                                     num_bathrooms_home=self.num_bathrooms_min,
                                                     num_bedrooms_home=self.num_bedrooms_min)

        self.home1 = RentDatabaseModel.objects.create(home_type_home=self.home_type,
                                                      price_home=self.price_middle,
                                                      move_in_day_home=self.move_in_day_home1,
                                                      num_bathrooms_home=self.num_bathrooms_middle,
                                                      num_bedrooms_home=self.num_bedrooms_max)
        self.home2 = RentDatabaseModel.objects.create(home_type_home=self.home_type1,
                                                      price_home=self.price_max,
                                                      move_in_day_home=self.move_in_day_home,
                                                      num_bathrooms_home=self.num_bathrooms_min,
                                                      num_bedrooms_home=self.num_bedrooms_min)
        self.home3 = RentDatabaseModel.objects.create(home_type_home=self.home_type1,
                                                      price_home=self.price_min,
                                                      move_in_day_home=self.move_in_day_home1,
                                                      num_bathrooms_home=self.num_bathrooms_max,
                                                      num_bedrooms_home=self.num_bedrooms_max)

        # Create some destination variables
        self.street_address = "12 Stony Brook Rd"
        self.city = "Arlington"
        self.state = "MA"
        self.zip_code = '02476'

    def tests_populate_survey_destinations_and_possible_homes_query_all_2_bedrooms_with_destination(self):
        # Arrange
        rent_algorithm = RentAlgorithm()
        # Create the survey
        survey = RentingSurveyModel.objects.create(
                                                   user_profile_survey=self.user_profile,
                                                   max_price_survey=self.price_max,
                                                   min_price_survey=self.price_min,
                                                   max_bathrooms_survey=self.max_bathrooms,
                                                   min_bathrooms_survey=self.min_bathrooms,
                                                   num_bedrooms_survey=self.num_bedrooms_min)
        survey.home_type_survey.set([self.home_type, self.home_type1])
        # Create a destination for the survey
        survey.rentingdestinationsmodel_set.create(street_address_destination=self.street_address,
                                                   city_destination=self.city,
                                                   state_destination=self.state,
                                                   zip_code_destination=self.zip_code)

        # Act
        rent_algorithm.populate_survey_destinations_and_possible_homes(survey)

        # Assert
        self.assertEqual(2, len(rent_algorithm.homes))
        self.assertEqual(1, len(rent_algorithm.destinations))
        self.assertEqual(self.home, rent_algorithm.homes[0].home)
        self.assertEqual(self.home2, rent_algorithm.homes[1].home)
