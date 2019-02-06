from django.test import TestCase

from cocoon.commutes.models import CommuteType
from cocoon.survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from cocoon.userAuth.models import MyUser, UserProfile
from cocoon.survey.models import RentingSurveyModel


class TestApproximateCommutesFilter(TestCase):

    def setUp(self):
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.survey = RentingSurveyModel.objects.create(user_profile=self.user.userProfile)

    def test_approximate_commute_filter_one_home_in_range(self):
        """
        Tests that if one home is in range then the function returns true
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        commute_algorithm = CommuteAlgorithm()
        commute_algorithm.approx_commute_range = 20

        approx_commute_times = {tenant: 40}

        # Act
        result = commute_algorithm.approximate_commute_filter(approx_commute_times)

        # Assert
        self.assertTrue(result)

    def test_approximate_commute_filter_one_home_too_far(self):
        """
        Tests that if one home is farther than the approximate_commute_range then the
            function returns false
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        commute_algorithm = CommuteAlgorithm()
        commute_algorithm.approx_commute_range = 20

        approx_commute_times = {tenant: 130}

        # Act
        result = commute_algorithm.approximate_commute_filter(approx_commute_times)

        # Assert
        self.assertFalse(result)

    def test_approximate_commute_filter_one_home_on_border(self):
        """
        Tests that if one home is equal to the max commute + commute range than the approximate_commute_range then the
            function returns true
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        commute_algorithm = CommuteAlgorithm()
        commute_algorithm.approx_commute_range = 20

        approx_commute_times = {tenant: 120}

        # Act
        result = commute_algorithm.approximate_commute_filter(approx_commute_times)

        # Assert
        self.assertTrue(result)

    def test_approximate_commute_filter_one_home_negative_commute(self):
        """
        Tests that if a home has a negative commute then the function returns false
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        commute_algorithm = CommuteAlgorithm()
        commute_algorithm.approx_commute_range = 20

        approx_commute_times = {tenant: -1}

        # Act
        result = commute_algorithm.approximate_commute_filter(approx_commute_times)

        # Assert
        self.assertFalse(result)

    def test_approximate_commute_filter_one_home_two_tenants_home_inside_both(self):
        """
        Tests that if a home is inside both of the tenants range than the function returns true
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        tenant1 = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=120,
            desired_commute=50,
        )

        commute_algorithm = CommuteAlgorithm()
        commute_algorithm.approx_commute_range = 20

        approx_commute_times = {tenant: 60,
                                tenant1: 40}

        # Act
        result = commute_algorithm.approximate_commute_filter(approx_commute_times)

        # Assert
        self.assertTrue(result)

    def test_approximate_commute_filter_one_home_two_tenants_home_inside_one_outside_other(self):
        """
        Tests if the home is inside one tenant but not the other than the function returns false
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        tenant1 = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=120,
            desired_commute=50,
        )

        commute_algorithm = CommuteAlgorithm()
        commute_algorithm.approx_commute_range = 20

        approx_commute_times = {tenant: 60,
                                tenant1: 145}

        # Act
        result = commute_algorithm.approximate_commute_filter(approx_commute_times)

        # Assert
        self.assertFalse(result)

    def test_approximate_commute_filter_one_home_two_tenants_home_outside_both(self):
        """
        Tests if the range is outside both tenants, then the function returns false
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        tenant1 = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=120,
            desired_commute=50,
        )

        commute_algorithm = CommuteAlgorithm()
        commute_algorithm.approx_commute_range = 20

        approx_commute_times = {tenant: 130,
                                tenant1: 145}

        # Act
        result = commute_algorithm.approximate_commute_filter(approx_commute_times)

        # Assert
        self.assertFalse(result)


class TestComputeCommuteScore(TestCase):

    def setUp(self):
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.survey = RentingSurveyModel.objects.create(user_profile=self.user.userProfile)

    def test_compute_commute_between_desired_and_max(self):
        """
        Tests that if the commute time is between the desired and max, the score is calculated,
            based on linear line
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 80

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(1 - (20/40), commute_score)

    def test_compute_commute_below_desired(self):
        """
        Tests that if the commute time is below desired then the home gets full points, i.e 1
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 50

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(1, commute_score)

    def test_compute_commute_above_max(self):
        """
        Tests that if the score is above the max, the home gets 0 points
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 110

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(0, commute_score)

    def test_compute_commute_below_min(self):
        """
        Tests that if the commute time is below the min then the home gets 100 points
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=60,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = -10

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(1, commute_score)

    def test_compute_commute_commute_equal_to_desired(self):
        """
        Tests that if the home is equal to the desired commute then it gets full points
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=50,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 50

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(1, commute_score)

    def test_compute_commute_commute_equal_to_max(self):
        """
        Tests that if the commute is equal to the max then it gets zero points
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=50,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 100

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(0, commute_score)

    def test_compute_commute_max_and_desired_equal_commute_equal(self):
        """
        Tests that if the max and desired are equal and the commute is equal to that,
            then the home gets full points
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=100,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 100

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(1, commute_score)

    def test_compute_commute_max_and_desired_commute_actual_commute_larger(self):
        """
        Tests that if the commute is greater but the max and desired are the same,
            then the home gets full points
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        tenant = self.survey.tenants.create(
            street_address="test",
            city="test",
            state="test",
            zip_code="test",
            commute_type=commute_type,
            commute_weight=0,
            max_commute=100,
            desired_commute=100,
        )

        # Commute information
        commute_score_algorithm = CommuteAlgorithm()
        commute_time = 110

        # Act
        commute_score = commute_score_algorithm.compute_commute_score(commute_time, tenant)

        # Assert
        self.assertEqual(1, commute_score)
