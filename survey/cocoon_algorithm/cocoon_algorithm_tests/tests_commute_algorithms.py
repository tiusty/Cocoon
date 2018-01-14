from django.test import TestCase

from houseDatabase.models import CommuteTypeModel
from survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from userAuth.models import MyUser, UserProfile
from survey.models import RentingSurveyModel


class TestApproximateCommutesFilter(TestCase):

    def setUp(self):
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='driving')
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
        approx_commutes_times = {self.destination.destination_key: 40}

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
        approx_commutes_times = {self.destination.destination_key: 110}

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
        approx_commutes_times = {self.destination.destination_key: 10}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_no_approx_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 50}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_no_approx_range_to_far(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 81}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_no_approx_range_to_close(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 39}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_at_max_distance(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 80}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_one_home_at_min_distance(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 40}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_in_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 45,
                                 self.destination1.destination_key: 70}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertTrue(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_one_out_of_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 45,
                                 self.destination1.destination_key: 90}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_both_out_of_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 30,
                                 self.destination1.destination_key: 90}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)

    def test_compute_approximate_commute_filter_multiple_home_in_range_with_approximate_range(self):
        # Arrange
        approx_algorithm = CommuteAlgorithm()
        approx_algorithm.approx_commute_range = 20
        approx_algorithm.min_user_commute = 40
        approx_algorithm.max_user_commute = 80
        approx_commutes_times = {self.destination.destination_key: 30,
                                 self.destination1.destination_key: 90}

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
        approx_commutes_times = {self.destination.destination_key: 10,
                                 self.destination1.destination_key: 101}

        # Act
        homes_in_range = approx_algorithm.compute_approximate_commute_filter(approx_commutes_times)

        # Assert
        self.assertFalse(homes_in_range)


class TestComputeCommuteScore(TestCase):

    def setUp(self):
        CommuteTypeModel.objects.create(commute_type_field='driving')

    def test_compute_commute_score_working(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        commute_score_algorithm.max_user_commute = 80
        commute_score_algorithm.min_user_commute = 30
        commute_time = 50

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time)

        # Assert
        self.assertEqual(1 - (20/50), commute_score)

    def test_compute_commute_less_than_min_commute(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        commute_score_algorithm.max_user_commute = 80
        commute_score_algorithm.min_user_commute = 30
        commute_time = 20

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time)

        # Assert
        self.assertEqual(1 - (0/50), commute_score)

    def test_compute_commute_more_than_max_commute(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        commute_score_algorithm.max_user_commute = 80
        commute_score_algorithm.min_user_commute = 30
        commute_time = 100

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time)

        # Assert
        self.assertEqual(1 - (50/50), commute_score)

    def test_compute_commute_equal_max_and_min_and_commute_not_equal(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        commute_score_algorithm.max_user_commute = 80
        commute_score_algorithm.min_user_commute = 80
        commute_time = 50

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time)

        # Assert
        self.assertEqual(1, commute_score)

    def test_compute_commute_equal_max_and_min_and_commute_equal(self):
        # Arrange
        commute_score_algorithm = CommuteAlgorithm()
        commute_score_algorithm.max_user_commute = 80
        commute_score_algorithm.min_user_commute = 80
        commute_time = 80

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time)

        # Assert
        self.assertEqual(1, commute_score)
