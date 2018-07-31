from django.test import TestCase

# Import survey modules
from cocoon.survey.cocoon_algorithm.price_algorithm import PriceAlgorithm


class TestPriceAlgorithm(TestCase):

    def test_compute_price_score_working(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.desired_price = 500
        price_algorithm.max_price = 2000
        home_price = 1000

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(1 - (500/1500), score_result)

    def test_compute_price_score_zero_desired_price(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.desired_price = 0
        price_algorithm.max_price = 1500
        home_price = 1000

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(1 - (1000/1500), score_result)

    def test_compute_price_score_zero_max_price(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.desired_price = 500
        price_algorithm.max_price = 0
        home_price = 1000

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(-1, score_result)

    def test_compute_price_score_zero_both_min_max_price(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.min_price = 0
        price_algorithm.max_price = 0
        home_price = 1000

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(-1, score_result)

    def test_compute_price_score_min_max_equal_price_of_home(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.min_price = 1000
        price_algorithm.max_price = 1000
        price_algorithm.desired_price = 1000
        home_price = 1000

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(1, score_result)

    def test_compute_price_score_min_max_equal_not_price_of_home(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.min_price = 1000
        price_algorithm.max_price = 1000
        home_price = 900

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(-1, score_result)

    def test_compute_price_score_zero_home_price(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.min_price = 500
        price_algorithm.max_price = 2000
        home_price = 0

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(-1, score_result)

    def test_compute_price_score_zero_home_price_both_zero_min_max_price(self):
        # Arrange
        price_algorithm = PriceAlgorithm()
        price_algorithm.min_price = 0
        price_algorithm.max_price = 0
        home_price = 0

        # Act
        score_result = price_algorithm.compute_price_score(home_price)

        # Assert
        self.assertEqual(1, score_result)
