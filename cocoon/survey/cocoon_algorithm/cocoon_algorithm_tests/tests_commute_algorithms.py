from django.test import TestCase

from cocoon.commutes.models import CommuteType
from cocoon.survey.cocoon_algorithm.commute_algorithms import CommuteAlgorithm
from cocoon.userAuth.models import MyUser, UserProfile
from cocoon.survey.models import RentingSurveyModel


class TestApproximateCommutesFilter(TestCase):

    def setUp(self):
        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile=self.user_profile)

        # Add renting destination
        self.street_address = '12 Stony Brook Rd'
        self.city = 'Arlington'
        self.state = 'MA'
        self.zip_code = '02476'
        self.commute_weight = 0

        self.street_address1 = '8 Stony Brook Rd'
        self.city1 = 'Arlington'
        self.state1 = 'MA'
        self.zip_code1 = '02476'
        self.commute_weight1 = 1
        self.min_commute1 = 10
        self.max_commute1 = 70

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
        # The actually commute type doesn't matter for the tests
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)

        # Create a user and survey so we can create renting destination models
        self.user = MyUser.objects.create(email="test@email.com")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.survey = RentingSurveyModel.objects.create(user_profile=self.user_profile)

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
        self.destination = self.survey.tenants.create(
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

        self.destination = self.survey.tenants.create(
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

        self.destination = self.survey.tenants.create(
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

        self.destination = self.survey.tenants.create(
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

        self.destination = self.survey.tenants.create(
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
