from django.test import TestCase

from cocoon.commutes.models import CommuteType
from cocoon.survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from cocoon.userAuth.models import MyUser, UserProfile
from cocoon.survey.models import RentingSurveyModel


class TestApproximateCommutesFilter(TestCase):

    def setUp(self):
        # The actually commute type doesn't matter for the tests
        self.commute_type = CommuteType.objects.create(commute_type='Driving')

        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile_survey=self.user_profile)

        # Add renting destination
        self.street_address = '12 Stony Brook Rd'
        self.city = 'Arlington'
        self.state = 'MA'
        self.zip_code = '02476'
        self.commute_type = self.commute_type
        self.commute_weight = 0
        self.min_commute = 40
        self.max_commute = 80
        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        self.street_address1 = '8 Stony Brook Rd'
        self.city1 = 'Arlington'
        self.state1 = 'MA'
        self.zip_code1 = '02476'
        self.commute_type1 = self.commute_type
        self.commute_weight1 = 1
        self.min_commute1 = 10
        self.max_commute1 = 70
        self.destination1 = self.survey.rentingdestinationsmodel_set.create(
            street_address=self.street_address1,
            city=self.city1,
            state=self.state1,
            zip_code=self.zip_code1,
            commute_type=self.commute_type1,
            commute_weight=self.commute_weight1,
            max_commute=self.max_commute1,
            min_commute=self.min_commute1,
        )

    def test_adding_positive_approx_commute_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = 30

        # Assert
        self.assertEqual(30, approx_algorithm.approx_commute_range)

    def test_adding_negative_approx_commute_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = -30

        # Assert
        self.assertEqual(0, approx_algorithm.approx_commute_range)

    def test_compute_approximate_commute_filter_one_home(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_times = 40
        approx_commutes_times = {self.destination: 40}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_to_far(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 110}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_to_close(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 10}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_no_approx_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 50}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_no_approx_range_to_far_zero_approx_commute_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_range = 0
        approx_commutes_times = {self.destination: 81}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_no_approx_range_to_close_zero_approx_commute_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_range = 0
        approx_commutes_times = {self.destination: 39}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_at_max_distance(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 80}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_at_min_distance(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 40}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_in_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 45,
                                 self.destination1: 70}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_one_out_of_range_zero_approx_commute_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_range = 0
        approx_commutes_times = {self.destination: 45,
                                 self.destination1: 90}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_both_out_of_range_zero_approx_commute_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_algorithm.approx_commute_range = 0
        approx_commutes_times = {self.destination: 30,
                                 self.destination1: 90}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_in_range_with_approximate_range_zero_approx_commute_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 30,
                                 self.destination1: 90}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_out_range_with_approximate_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination: 10,
                                 self.destination1: 101}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)


class TestComputeCommuteScore(TestCase):

    def setUp(self):
        # The actually commute type doesn't matter for the tests
        self.commute_type = CommuteType.objects.create(commute_type='Driving')

        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile_survey=self.user_profile)

        # Add renting destination
        self.street_address = '12 Stony Brook Rd'
        self.city = 'Arlington'
        self.state = 'MA'
        self.zip_code = '02476'
        self.commute_type = self.commute_type
        self.commute_weight = 0

    def test_compute_commute_score_working(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 50

        self.min_commute = 30
        self.max_commute = 80
        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, self.destination)

        # Assert
        self.assertEqual(1 - (20/50), commute_score)

    def test_compute_commute_less_than_min_commute(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        self.max_commute = 80
        self.min_commute = 30
        commute_time = 20

        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, self.destination)

        # Assert
        self.assertEqual(1 - (0/50), commute_score)

    def test_compute_commute_more_than_max_commute(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        self.max_commute = 80
        self.min_commute = 30
        commute_time = 100

        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, self.destination)

        # Assert
        self.assertEqual(1 - (50/50), commute_score)

    def test_compute_commute_equal_max_and_min_and_commute_not_equal(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        self.max_commute = 80
        self.min_commute = 80
        commute_time = 50

        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, self.destination)

        # Assert
        self.assertEqual(1, commute_score)

    def test_compute_commute_equal_max_and_min_and_commute_equal(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        self.max_commute = 80
        self.min_commute = 80
        commute_time = 80

        self.destination = self.survey.rentingdestinationsmodel_set.create(
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            commute_type=self.commute_type,
            commute_weight=self.commute_weight,
            max_commute=self.max_commute,
            min_commute=self.min_commute,
        )

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, self.destination)

        # Assert
        self.assertEqual(1, commute_score)
