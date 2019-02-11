from django.test import TestCase

# Import survey modules
from cocoon.survey.cocoon_algorithm.weighted_scoring_algorithm import WeightScoringAlgorithm, HYBRID_WEIGHT_MAX
from cocoon.userAuth.models import MyUser
from cocoon.houseDatabase.models import HomeProviderModel, HomeTypeModel, RentDatabaseModel
from cocoon.survey.models import RentingSurveyModel
from cocoon.survey.home_data.home_score import HomeScore

# Import global config parameters
from cocoon.survey.constants import HYBRID_WEIGHT_MAX, HYBRID_WEIGHT_MIN, HYBRID_QUESTION_WEIGHT


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
        user_scale_factor = 3
        does_contain_item = False

        # Act
        result = weighted_algorithm.compute_weighted_question_score(user_scale_factor, does_contain_item)

        # Assert
        self.assertEqual(0, result)

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


class TestLaundryWeightingQuestion(TestCase):

    def setUp(self):
        # Create a user so the survey form can validate
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2, wants_laundry_in_building=False, wants_laundry_in_unit=False,
                      laundry_in_building_weight=0, laundry_in_unit_weight=0):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
            wants_laundry_in_building=wants_laundry_in_building,
            wants_laundry_in_unit=wants_laundry_in_unit,
            laundry_in_unit_weight=laundry_in_unit_weight,
            laundry_in_building_weight=laundry_in_building_weight,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2,
                    zip_code="02476", state="MA", latitude=0.0, longitude=0.0,
                    laundry_in_building=False, laundry_in_unit=False):
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
            laundry_in_unit=laundry_in_unit,
            laundry_in_building=laundry_in_building,
        ))

    def test_wants_neither_in_unit_and_building(self):
        """
        Tests that if a user says they don't want in building or in unit then
            even if the home has it, it doesn't affect the score
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile, wants_laundry_in_building=False, wants_laundry_in_unit=False)
        weighted_algorithm = WeightScoringAlgorithm()

        home = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=True)

        # Act
        weighted_algorithm.handle_laundry_weight_question(survey, home)

        # Assert
        self.assertEqual(home.accumulated_points, 0)
        self.assertEqual(home.total_possible_points, 0)
        self.assertFalse(home.eliminated)

    def test_wants_in_unit_not_need(self):
        """
        Tests that if the user needs in building, then if the home has either in unit or in building
            then it is scored properly
        """
        # Arrange
        in_unit_weight = HYBRID_WEIGHT_MAX - 1
        in_building_weight = 0
        survey = self.create_survey(self.user.userProfile, wants_laundry_in_building=False,
                                    wants_laundry_in_unit=True,
                                    laundry_in_unit_weight=in_unit_weight,
                                    laundry_in_building_weight=in_building_weight,
                                    )
        weighted_algorithm = WeightScoringAlgorithm()

        # Create homes
        home = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=False)
        home1 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=False)
        home2 = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=True)
        home3 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=True)

        # Act
        weighted_algorithm.handle_laundry_weight_question(survey, home)
        weighted_algorithm.handle_laundry_weight_question(survey, home1)
        weighted_algorithm.handle_laundry_weight_question(survey, home2)
        weighted_algorithm.handle_laundry_weight_question(survey, home3)

        # Assert
        self.assertEqual(home.accumulated_points, 0)
        self.assertEqual(home.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home.eliminated)

        self.assertEqual(home1.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_unit_weight, home1.home.laundry_in_unit))
        self.assertEqual(home1.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home1.eliminated)

        self.assertEqual(home2.accumulated_points, 0)
        self.assertEqual(home2.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home2.eliminated)

        self.assertEqual(home3.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_unit_weight, home3.home.laundry_in_unit))
        self.assertEqual(home3.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home3.eliminated)

    def test_wants_in_unit_need(self):
        """
        Tests that if the user needs in building, then if the home has either in unit or in building
            then it is scored properly
        """
        # Arrange
        in_unit_weight = HYBRID_WEIGHT_MAX
        in_building_weight = 0
        survey = self.create_survey(self.user.userProfile, wants_laundry_in_building=False,
                                    wants_laundry_in_unit=True,
                                    laundry_in_unit_weight=in_unit_weight,
                                    laundry_in_building_weight=in_building_weight,
                                    )
        weighted_algorithm = WeightScoringAlgorithm()

        # Create homes
        home = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=False)
        home1 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=False)
        home2 = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=True)
        home3 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=True)

        # Act
        weighted_algorithm.handle_laundry_weight_question(survey, home)
        weighted_algorithm.handle_laundry_weight_question(survey, home1)
        weighted_algorithm.handle_laundry_weight_question(survey, home2)
        weighted_algorithm.handle_laundry_weight_question(survey, home3)

        # Assert
        self.assertEqual(home.accumulated_points, 0)
        self.assertEqual(home.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertTrue(home.eliminated)

        self.assertEqual(home1.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_unit_weight, home1.home.laundry_in_unit))
        self.assertEqual(home1.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home1.eliminated)

        self.assertEqual(home2.accumulated_points, 0)
        self.assertEqual(home2.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertTrue(home2.eliminated)

        self.assertEqual(home3.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_unit_weight, home3.home.laundry_in_unit))
        self.assertEqual(home3.total_possible_points, abs(in_unit_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home3.eliminated)

    def test_wants_in_building_not_need(self):
        """
        Tests that if the user needs in building, then if the home has either in unit or in building
            then it is scored properly
        """
        # Arrange
        in_unit_weight = 0
        in_building_weight = HYBRID_WEIGHT_MAX - 1
        survey = self.create_survey(self.user.userProfile, wants_laundry_in_building=True,
                                    wants_laundry_in_unit=False,
                                    laundry_in_unit_weight=in_unit_weight,
                                    laundry_in_building_weight=in_building_weight,
                                    )
        weighted_algorithm = WeightScoringAlgorithm()

        # Create homes
        home = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=False)
        home1 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=False)
        home2 = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=True)
        home3 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=True)

        # Act
        weighted_algorithm.handle_laundry_weight_question(survey, home)
        weighted_algorithm.handle_laundry_weight_question(survey, home1)
        weighted_algorithm.handle_laundry_weight_question(survey, home2)
        weighted_algorithm.handle_laundry_weight_question(survey, home3)

        # Assert
        self.assertEqual(home.accumulated_points, 0)
        self.assertEqual(home.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home.eliminated)

        self.assertEqual(home1.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_building_weight, home1.home.laundry_in_unit))
        self.assertEqual(home1.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home1.eliminated)

        self.assertEqual(home2.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_building_weight, home2.home.laundry_in_building))
        self.assertEqual(home2.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home2.eliminated)

        self.assertEqual(home3.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_building_weight, home3.home.laundry_in_unit))
        self.assertEqual(home3.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home3.eliminated)

    def test_wants_in_building_need(self):
        """
        Tests that if the user needs in building, then if the home has either in unit or in building
            then it is not eliminated and scored properly
        """
        # Arrange
        in_unit_weight = 0
        in_building_weight = HYBRID_WEIGHT_MAX
        survey = self.create_survey(self.user.userProfile, wants_laundry_in_building=True,
                                    wants_laundry_in_unit=False,
                                    laundry_in_unit_weight=in_unit_weight,
                                    laundry_in_building_weight=in_building_weight,
                                    )
        weighted_algorithm = WeightScoringAlgorithm()

        # Create homes
        home = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=False)
        home1 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=False)
        home2 = self.create_home(self.home_type, laundry_in_unit=False, laundry_in_building=True)
        home3 = self.create_home(self.home_type, laundry_in_unit=True, laundry_in_building=True)

        # Act
        weighted_algorithm.handle_laundry_weight_question(survey, home)
        weighted_algorithm.handle_laundry_weight_question(survey, home1)
        weighted_algorithm.handle_laundry_weight_question(survey, home2)
        weighted_algorithm.handle_laundry_weight_question(survey, home3)

        # Assert
        self.assertEqual(home.accumulated_points, 0)
        self.assertEqual(home.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertTrue(home.eliminated)

        self.assertEqual(home1.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_building_weight, home1.home.laundry_in_unit))
        self.assertEqual(home1.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home1.eliminated)

        self.assertEqual(home2.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_building_weight, home2.home.laundry_in_building))
        self.assertEqual(home2.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home2.eliminated)

        self.assertEqual(home3.accumulated_points, weighted_algorithm.compute_weighted_question_score(in_building_weight, home3.home.laundry_in_unit))
        self.assertEqual(home3.total_possible_points, abs(in_building_weight) * weighted_algorithm.hybrid_question_weight)
        self.assertFalse(home3.eliminated)
