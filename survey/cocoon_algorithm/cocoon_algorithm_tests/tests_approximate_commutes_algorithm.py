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

    def test_compute_approximate_commute_score(self):
        # Arrange
        approx_algorithm = ApproximateCommutes()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 40
        approx_algorithm.approx_commute_times = 50

        # Act
        home_in_range = approx_algorithm.compute_approximate_commute_score()

        # Assert
        self.assertTrue(home_in_range)


