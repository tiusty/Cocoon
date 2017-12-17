from django.test import TestCase

# Import survey python modules
from survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from survey.home_data.home_score import HomeScore

# Import external models
from houseDatabase.models import RentDatabase


class TestRentAlgorithm(TestCase):

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
        rent_algorithm.run_compute_approximate_commute_score()

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
        rent_algorithm.run_compute_approximate_commute_score()

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
        rent_algorithm.run_compute_approximate_commute_score()

        # Assert
        self.assertTrue(rent_algorithm.homes[0].eliminated)
        self.assertTrue(rent_algorithm.homes[1].eliminated)
        self.assertTrue(rent_algorithm.homes[2].eliminated)

    def test_run_compute_approximate_commute_score_no_homes(self):
        # Arrange
        rent_algorithm = RentAlgorithm()

        # Act
        rent_algorithm.run_compute_approximate_commute_score()

        # Assert
        self.assertEqual(0, len(rent_algorithm.homes))
