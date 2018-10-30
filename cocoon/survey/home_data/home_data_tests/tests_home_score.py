# Django imports
from django.test import TestCase
from django.utils import timezone
from unittest.mock import MagicMock

from cocoon.survey.home_data.home_score import HomeScore
from cocoon.userAuth.models import MyUser
from cocoon.survey.models import RentingDestinationsModel, RentingSurveyModel
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, HomeProviderModel
from cocoon.commutes.models import ZipCodeBase, CommuteType
from cocoon.commutes.constants import ZIP_CODE_TIMEDELTA_VALUE
from cocoon.survey.constants import AVERAGE_BICYCLING_SPEED, AVERAGE_WALKING_SPEED


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


class TestApproxCommute(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.rentingdestinationsmodel_set.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,

        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2,
                    zip_code="02476", state="MA", latitude=0.0, longitude=0.0):
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
        ))

    @staticmethod
    def create_zip_code_dictionary(zip_code):
        return ZipCodeBase.objects.create(zip_code=zip_code)

    @staticmethod
    def create_zip_code_dictionary_child(parent_zip_code_dictionary, zip_code, commute_time,
                                         commute_distance, commute_type, last_updated=timezone.now()):
        parent_zip_code_dictionary.zipcodechild_set.create(
            zip_code=zip_code,
            commute_time_seconds=commute_time,
            commute_distance_meters=commute_distance,
            commute_type=commute_type,
            last_date_updated=last_updated,
        )

    def test_populate_approx_commute_times_driving(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type)
        home.zip_code_approximation = MagicMock()
        home.lat_lng_approximation = MagicMock()

        # Act
        home.populate_approx_commutes(home.home, destination)

        # Assert
        home.zip_code_approximation.assert_called_once_with(home.home.zip_code, destination)
        home.lat_lng_approximation.assert_not_called()

    def test_populate_approx_commute_times_transit(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        commute_type_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)
        destination = self.create_destination(survey, commute_type_transit)
        home.zip_code_approximation = MagicMock()
        home.lat_lng_approximation = MagicMock()

        # Act
        home.populate_approx_commutes(home.home, destination)

        # Assert
        home.zip_code_approximation.assert_called_once_with(home.home.zip_code, destination)
        home.lat_lng_approximation.assert_not_called()

    def test_populate_approx_commute_times_bicycling(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        commute_type_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        destination = self.create_destination(survey, commute_type_bicycling)
        latlng = (5,10)
        home.zip_code_approximation = MagicMock()
        home.lat_lng_approximation = MagicMock()

        # Act
        home.populate_approx_commutes(home.home, destination, lat_lng_dest=latlng)

        # Assert
        home.zip_code_approximation.assert_not_called()
        home.lat_lng_approximation.assert_called_once_with(home.home, destination, latlng, AVERAGE_BICYCLING_SPEED)

    def test_populate_approx_commute_times_walking(self):
        # Arrange
        home = self.create_home(self.home_type)
        survey = self.create_survey(self.user.userProfile)
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        destination = self.create_destination(survey, commute_type_walking)
        latlng = (5,10)
        home.zip_code_approximation = MagicMock()
        home.lat_lng_approximation = MagicMock()

        # Act
        home.populate_approx_commutes(home.home, destination, lat_lng_dest=latlng)

        # Assert
        home.zip_code_approximation.assert_not_called()
        home.lat_lng_approximation.assert_called_once_with(home.home, destination, latlng, AVERAGE_WALKING_SPEED)

    def test_zip_code_approximation_combo_exists(self):
        """
        Tests that if the zip_combo exists then it will extract it from the zip-code database and use the values
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="100 Main Street")
        zip_code = '02476'
        home = self.create_home(self.home_type)
        commute_distance = 100
        commute_time_seconds = 376

        # Create the zip-code dictionary
        parent_zip_code = self.create_zip_code_dictionary(zip_code)
        self.create_zip_code_dictionary_child(parent_zip_code, destination.zip_code, commute_time_seconds,
                                              commute_distance, self.commute_type)

        # Act
        result = home.zip_code_approximation(zip_code, destination)

        # Assert
        self.assertTrue(result)
        # Convert to minutes because that is what is returned
        self.assertEqual(home.approx_commute_times, {destination: commute_time_seconds / 60})

    def test_zip_code_approximation_child_does_not_exist(self):
        """
        Tests that if the parent zip code exists but not the child, then the function will return false
            and the home will not be added to the list of commute times
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="100 Main Street")
        zip_code = '02476'
        home = self.create_home(self.home_type)

        # Create the zip-code dictionary
        self.create_zip_code_dictionary(zip_code)

        # Act
        result = home.zip_code_approximation(zip_code, destination)

        # Assert
        self.assertFalse(result)
        # Convert to minutes because that is what is returned
        self.assertEqual(home.approx_commute_times, {})

    def test_zip_code_approximation_neither_exist(self):
        """
        Tests that if the parent/child zip code approximation doesn't exist then the function will return false and
            the commute is not added to the approx_commute_times
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="100 Main Street")
        zip_code = '02476'
        home = self.create_home(self.home_type)

        # Act
        result = home.zip_code_approximation(zip_code, destination)

        # Assert
        self.assertFalse(result)
        # Convert to minutes because that is what is returned
        self.assertEqual(home.approx_commute_times, {})

    def test_zip_code_approximation_exit_not_valid(self):
        """
        Tests that if the parent/child zip code pair exists but are out of date then the commute is not added
            and the function returns false
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        destination = self.create_destination(survey, self.commute_type, street_address="100 Main Street")
        zip_code = '02476'
        home = self.create_home(self.home_type)
        commute_distance = 100
        commute_time_seconds = 376

        # Create the zip-code dictionary
        parent_zip_code = self.create_zip_code_dictionary(zip_code)
        self.create_zip_code_dictionary_child(parent_zip_code, destination.zip_code, commute_time_seconds,
                                              commute_distance, self.commute_type,
                                              last_updated=timezone.now() -
                                                           timezone.timedelta(days=ZIP_CODE_TIMEDELTA_VALUE + 1))

        # Act
        result = home.zip_code_approximation(zip_code, destination)

        # Assert
        self.assertFalse(result)
        # Convert to minutes because that is what is returned
        self.assertEqual(home.approx_commute_times, {})

    def test_lat_lng_approximation_bicycling(self):
        """
        Tests that the lat_lng approximation for for bicycling
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type, latitude=42.399305, longitude=-71.135242)
        commute_type_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        destination = self.create_destination(survey, commute_type_bicycling)

        # Act
        result = home.lat_lng_approximation(home.home, destination, (42.4080528, -71.1632442),
                                            average_speed=AVERAGE_BICYCLING_SPEED)

        # Assert
        self.assertTrue(result)
        self.assertAlmostEqual(home.approx_commute_times[destination], 17.8878, places=3)

    def test_lat_lng_approximation_walking(self):
        """
        Tests that the lat lng approximation works for walking
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type, latitude=42.399305, longitude=-71.135242)
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        destination = self.create_destination(survey, commute_type_walking)

        # Act
        result = home.lat_lng_approximation(home.home, destination, (42.4080528, -71.1632442),
                                            average_speed=AVERAGE_WALKING_SPEED)

        # Assert
        self.assertTrue(result)
        self.assertAlmostEqual(home.approx_commute_times[destination], 39.6506, places=3)

    def test_lat_lng_approximation_average_speed_zero(self):
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home = self.create_home(self.home_type, latitude=42.408021, longitude=-71.163222)
        commute_type_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        destination = self.create_destination(survey, commute_type_walking)

        # Act
        result = home.lat_lng_approximation(home.home, destination, (42.415656, -71.165393),
                                            average_speed=0)

        # Assert
        self.assertFalse(result)
        self.assertEqual(home.approx_commute_times, {})


