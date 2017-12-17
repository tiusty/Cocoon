from django.test import TestCase

from survey.cocoon_algorithm.approximate_commutes_algorithm import ApproximateCommutes


class TestApproximateCommutes(TestCase):

    def test_adding_approx_commute_times(self):
        # Arrange
        approx_algo = ApproximateCommutes()
        self.assertEqual(0, len(approx_algo.approx_commute_times))
        approx_algo.approx_commute_times = 20
        approx_algo.approx_commute_times = 40

        # Act
        num_approx_commutes = len(approx_algo.approx_commute_times)

        # Assert
        self.assertEqual(2, num_approx_commutes)

    def test_adding_positive_approx_commute_range(self):
        # Arrange
        approx_algo = ApproximateCommutes()
        approx_algo.approx_commute_range = 30

        # Assert
        self.assertEqual(30, approx_algo.approx_commute_range)

    def test_adding_negative_approx_commute_range(self):
        # Arrange
        approx_algo = ApproximateCommutes()
        approx_algo.approx_commute_range = -30

        # Assert
        self.assertEqual(0, approx_algo.approx_commute_range)

    def test_compute_approximate_commute_score_one_home(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 40

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_score_one_home_to_far(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 110

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_score_one_home_to_close(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 10

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_score_one_home_no_approx_range(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 50

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_score_one_home_no_approx_range_to_far(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 81

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_score_one_home_no_approx_range_to_close(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 39

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_score_one_home_at_max_distance(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 80

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_score_one_home_at_min_distance(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 40

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_score_multiple_home_in_range(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 45
        approx_algorithm.approx_commute_times = 70

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_score_multiple_home_one_out_of_range(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 45
        approx_algorithm.approx_commute_times = 90

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_score_multiple_home_both_out_of_range(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 30
        approx_algorithm.approx_commute_times = 90

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_score_multiple_home_in_range_with_approximate_range(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 30
        approx_algorithm.approx_commute_times = 90

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_score_multiple_home_out_range_with_approximate_range(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 10
        approx_algorithm.approx_commute_times = 101

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertFalse(homes_in_range)
