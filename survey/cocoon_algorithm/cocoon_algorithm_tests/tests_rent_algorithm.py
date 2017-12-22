from django.test import TestCase

# Import survey python modules
from survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from survey.home_data.home_score import HomeScore

# Import external models
from houseDatabase.models import RentDatabase


class TestRentAlgorithmJustApproximateCommuteFilter(TestCase):

    def setUp(self):
        self.home = HomeScore(RentDatabase.objects.create())
        self.home.approx_commute_times = 50
        self.home.approx_commute_times = 70
        self.home1 = HomeScore(RentDatabase.objects.create())
        self.home1.approx_commute_times = 10
        self.home1.approx_commute_times = 70
        self.home2 = HomeScore(RentDatabase.objects.create())
        self.home2.approx_commute_times = 40
        self.home2.approx_commute_times = 100

    def test_run_compute_approximate_commute_score_no_eliminations(self):
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

    def test_run_compute_approximate_commute_score_one_elimination(self):
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

    def test_run_compute_approximate_commute_score_all_eliminated(self):
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

    def test_run_compute_approximate_commute_score_no_homes(self):
        # Arrange
        rent_algorithm = RentAlgorithm()

        # Act
        rent_algorithm.run_compute_approximate_commute_filter()

        # Assert
        self.assertEqual(0, len(rent_algorithm.homes))


class TestRentAlgorithmJustPrice(TestCase):

    def setUp(self):
        self.home = HomeScore(RentDatabase.objects.create(price=1000))
        self.home1 = HomeScore(RentDatabase.objects.create(price=1500))
        self.home2 = HomeScore(RentDatabase.objects.create(price=2000))

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
        self.assertEqual((1 - (0/1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertFalse(rent_algorithm.homes[0].eliminated)
        self.assertEqual((1 - (500/1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)
        self.assertEqual((1 - (1000/1500)) * price_question_weight * price_user_scale_factor,
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
        self.assertEqual((1 - (400/1400)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual((1 - (900/1400)) * price_question_weight * price_user_scale_factor,
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
        self.assertEqual((1 - (400/900)) * price_question_weight * price_user_scale_factor,
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
        self.assertEqual((1 - (0/900)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertFalse(rent_algorithm.homes[0].eliminated)

        # Home 1
        self.assertEqual((1 - (500/900)) * price_question_weight * price_user_scale_factor,
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
        self.assertEqual((1 - (0/400)) * price_question_weight * price_user_scale_factor,
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
        self.assertEqual((1 - (0/1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[0].total_possible_points)
        self.assertFalse(rent_algorithm.homes[0].eliminated)

        # Home 1
        self.assertEqual((1 - (500/1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[1].total_possible_points)
        self.assertFalse(rent_algorithm.homes[1].eliminated)

        # Home 2
        self.assertEqual((1 - (1000/1500)) * price_question_weight * price_user_scale_factor,
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(price_question_weight * price_user_scale_factor, rent_algorithm.homes[2].total_possible_points)
        self.assertFalse(rent_algorithm.homes[2].eliminated)


class TestRentAlgorithmJustApproximateCommuteScore(TestCase):

    def setUp(self):
        self.home = HomeScore(RentDatabase.objects.create())
        self.home.approx_commute_times = 50
        self.home.approx_commute_times = 70
        self.home1 = HomeScore(RentDatabase.objects.create())
        self.home1.approx_commute_times = 10
        self.home1.approx_commute_times = 80
        self.home1.approx_commute_times = 100
        self.home2 = HomeScore(RentDatabase.objects.create())
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
        self.assertEqual(((1 - (0/60)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (20/60)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[0].approx_commute_times) * (commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0/60)) * commute_question_weight * commute_user_scale_factor)
                         + ((1 - (30/60)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (50/60)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[1].approx_commute_times) * (commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (10/60)) * commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[2].approx_commute_times) * (commute_question_weight * commute_user_scale_factor),
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
        self.assertEqual(((1 - (20/70)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (40/70)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[0].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[0].approx_commute_times) * (commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[0].total_possible_points)

        # Home 1
        self.assertEqual(((1 - (0/70)) * commute_question_weight * commute_user_scale_factor)
                         + ((1 - (50/70)) * commute_user_scale_factor * commute_question_weight)
                         + ((1 - (70/70)) * commute_user_scale_factor * commute_question_weight),
                         rent_algorithm.homes[1].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[1].approx_commute_times) * (commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[1].total_possible_points)

        # Home 2
        self.assertEqual(((1 - (30/70)) * commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[2].accumulated_points)
        self.assertEqual(len(rent_algorithm.homes[2].approx_commute_times) * (commute_question_weight * commute_user_scale_factor),
                         rent_algorithm.homes[2].total_possible_points)
