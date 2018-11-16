# Django imports
from django.test import TestCase
from django.utils import timezone
from unittest.mock import MagicMock

from cocoon.survey.home_data.home_score import HomeScore
from cocoon.userAuth.models import MyUser
from cocoon.survey.models import RentingSurveyModel
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, HomeProviderModel
from cocoon.commutes.models import ZipCodeBase, CommuteType
from cocoon.commutes.constants import ZIP_CODE_TIMEDELTA_VALUE


class TestScoringMethods(TestCase):

    def setUp(self):
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    def test_percent_score_positive(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual((accumulated_points/total_possible_points) * 100, home_score.percent_score())

    def test_percent_score_positive_eliminated(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_negative(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = -20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_negative_eliminated(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = -20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_negative(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 20
        total_possible_points = -30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_negative_eliminated(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 20
        total_possible_points = -30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_zero(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 0
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(0, home_score.percent_score())

    def test_percent_score_accumulated_points_zero_eliminated(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 0
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_zero(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 30
        total_possible_points = 0

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(0, home_score.percent_score())

    def test_percent_score_total_possible_points_zero_eliminated(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 30
        total_possible_points = 0

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_eliminate_home(self):
        # Arrange // not really following methodology
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        self.assertFalse(home_score.eliminated)
        home_score.eliminate_home()
        self.assertTrue(home_score.eliminated)

    def test_user_friendly_score(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        accumulated_points = 20
        total_possible_points = 50

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(round((accumulated_points/total_possible_points)*100), home_score.user_friendly_score())

    def test_home_setter_constructor(self):
        # Arrange
        self.home = self.create_home(self.home_type)
        home_score = HomeScore(self.home)

        # Assert
        self.assertIsNotNone(home_score.home)

    def test_home_setter_later(self):
        # Arrange // Note really following methodology
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        self.assertIsNone(home_score.home)
        home_score.home = self.home
        self.assertIsNotNone(home_score.home)

    def test_approx_commute_times_setter_basic(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        self.assertEqual(home_score.approx_commute_times, {})

        # Act
        home_score.approx_commute_times = {"12345": 10}
        home_score.approx_commute_times = {"01234": 20}

        # Assert
        self.assertEqual(home_score.approx_commute_times, {"12345": 10, "01234": 20})

    def test_approx_commute_times_setter_overwriting(self):
        # Arrange
        home_score = HomeScore()
        self.home = self.create_home(self.home_type)
        self.assertEqual(home_score.approx_commute_times, {})

        # Act
        home_score.approx_commute_times = {"12345": 10}
        home_score.approx_commute_times = {"01234": 20}
        home_score.approx_commute_times = {}
        home_score.approx_commute_times = {"12345": 50}

        # Assert
        self.assertEqual(home_score.approx_commute_times, {"12345": 50, "01234": 20})


