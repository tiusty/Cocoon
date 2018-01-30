from django.test import TestCase
from survey.home_data.home_score import HomeScore
from survey.models import RentingSurveyModel, DestinationsModel, RentingDestinationsModel
from houseDatabase.models import RentDatabaseModel, ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel, \
    HomeTypeModel, CommuteTypeModel

class TestScoringMethods(TestCase):

    def setUp(self):
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = RentDatabaseModel.objects.create(home_type_home=self.home_type)

    def test_percent_score_positive(self):
        # Arrange
        home_score = HomeScore()
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
        self.assertFalse(home_score.eliminated)
        home_score.eliminate_home()
        self.assertTrue(home_score.eliminated)

    def test_user_friendly_score(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = 50

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(round((accumulated_points/total_possible_points)*100), home_score.user_friendly_score())

    def test_home_setter_constructor(self):
        # Arrange
        home_score = HomeScore(self.home)

        # Assert
        self.assertIsNotNone(home_score.home)

    def test_home_setter_later(self):
        # Arrange // Note really following methodology
        home_score = HomeScore()
        self.assertIsNone(home_score.home)
        home_score.home = self.home
        self.assertIsNotNone(home_score.home)

    def test_approx_commute_times_setter_basic(self):
        # Arrange
        home_score = HomeScore()
        self.assertEqual(home_score.approx_commute_times, {})

        # Act
        home_score.approx_commute_times = {"12345": 10}
        home_score.approx_commute_times = {"01234": 20}

        # Assert
        self.assertEqual(home_score.approx_commute_times, {"12345": 10, "01234": 20})

    def test_approx_commute_times_setter_overwriting(self):
        # Arrange
        home_score = HomeScore()
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
        self.zip_code = "12345"
        self.zip_code1 = "01234"
        self.zip_code2 = "23456"
        self.commute_time = 6000 
        self.commute_distance = 700
        self.commute_type = CommuteTypeModel.objects.create(commute_type_field='driving')
        self.commute_type_walking = CommuteTypeModel.objects.create(commute_type_field='walking')

    @staticmethod
    def create_destination(address, city, state, zip):
        return RentingDestinationsModel.objects.create(
            survey_destinations_id="0",
            street_address_destination=address,
            city_destination=city,
            state_destination=state,
            zip_code_destination=zip
        )

    @staticmethod
    def create_zip_code_dictionary(zip_code):
        return ZipCodeDictionaryParentModel.objects.create(zip_code_parent=zip_code)

    @staticmethod
    def create_zip_code_dictionary_child(parent_zip_code_dictionary, zip_code, commute_time, 
                                         commute_distance, commute_type):
        parent_zip_code_dictionary.zipcodedictionarychildmodel_set.create(
                zip_code_child=zip_code,
                commute_time_seconds_child=commute_time,
                commute_distance_meters_child=commute_distance,
                commute_type_child=commute_type,
                )

    def test_populate_approx_commute_times(self):
        # Arrange
        home_score = HomeScore()
        destination = self.create_destination("101 Test Street", "Los Angeles", "California", self.zip_code1)
        destination1 = self.create_destination("101 Test Street", "Los Angeles", "California", self.zip_code2)
        destination2 = self.create_destination("101 Test Street", "Los Angeles", "California", self.zip_code)
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code1, self.commute_time,
                                              self.commute_distance, self.commute_type)

        # Act
        ret1 = home_score.populate_approx_commutes(self.zip_code, destination, self.commute_type)
        ret2 = home_score.populate_approx_commutes(self.zip_code, destination1, self.commute_type)
        ret3 = home_score.populate_approx_commutes("00000", destination, self.commute_type)
        ret4 = home_score.populate_approx_commutes(self.zip_code, destination2, self.commute_type_walking)

        # Assert
        self.assertEqual(ret1, True)
        self.assertEqual(home_score.approx_commute_times, {"101 Test Street-Los Angeles-California-01234": 100.0})
        self.assertEqual(ret2, False)
        self.assertEqual(ret3, False)
        self.assertEqual(ret4, False)