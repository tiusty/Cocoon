from django.test import TestCase

# Import survey modules
from cocoon.survey.cocoon_algorithm.weighted_scoring_algorithm import WeightScoringAlgorithm

# Import global config parameters
from config.settings.Global_Config import HYBRID_WEIGHT_MAX, HYBRID_WEIGHT_MIN, HYBRID_QUESTION_WEIGHT


class TestWeightedScoringAlgorithmFilter(TestCase):

    def test_compute_weighted_question_filter_working(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()

        # Act
        result = weighted_algorithm.compute_weighted_question_filter(0, True)

        # Assert
        self.assertTrue(result)

    def test_compute_weighted_question_filter_hybrid_max_contains_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()

        # Act
        result = weighted_algorithm.compute_weighted_question_filter(HYBRID_WEIGHT_MAX, True)

        # Assert
        self.assertTrue(result)

    def test_compute_weighted_question_filter_hybrid_max_does_not_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()

        # Act
        result = weighted_algorithm.compute_weighted_question_filter(HYBRID_WEIGHT_MAX, False)

        # Assert
        self.assertFalse(result)

    def test_compute_weighted_question_filter_hybrid_min_contains_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()

        # Act
        result = weighted_algorithm.compute_weighted_question_filter(HYBRID_WEIGHT_MIN, True)

        # Assert
        self.assertFalse(result)

    def test_compute_weighted_question_filter_hybrid_min_does_not_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()

        # Act
        result = weighted_algorithm.compute_weighted_question_filter(HYBRID_WEIGHT_MIN, False)

        # Assert
        self.assertTrue(result)


class TestWeightedScoringAlgorithmScoring(TestCase):

    def test_compute_weighted_question_score_working(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()
        user_scale_factor = 1
        does_contain_item = True

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(1 * user_scale_factor * HYBRID_QUESTION_WEIGHT, result)

    def test_compute_weighted_question_score_positive_scale_factor_does_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()
        user_scale_factor = 4
        does_contain_item = True

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(1 * user_scale_factor * HYBRID_QUESTION_WEIGHT, result)

    def test_compute_weighted_question_score_positive_scale_factor_does_not_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()
        user_scale_factor = 4
        does_contain_item = False

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(-1 * user_scale_factor * HYBRID_QUESTION_WEIGHT, result)

    def test_compute_weighted_question_score_negative_scale_factor_does_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()
        user_scale_factor = -2
        does_contain_item = True

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(1 * user_scale_factor * HYBRID_QUESTION_WEIGHT, result)

    def test_compute_weighted_question_score_negative_scale_factor_does_not_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()
        user_scale_factor = -2
        does_contain_item = False

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(-1 * user_scale_factor * HYBRID_QUESTION_WEIGHT, result)

    def test_compute_weighted_question_score_zero_scale_factor_does_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()
        user_scale_factor = 0
        does_contain_item = True

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(0, result)

    def test_compute_weighted_question_score_zero_scale_factor_does_not_contain_item(self):
        # Arrange
        weighted_algorithm = WeightScoringAlgorithm()
        user_scale_factor = 0
        does_contain_item = False

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(0, result)
