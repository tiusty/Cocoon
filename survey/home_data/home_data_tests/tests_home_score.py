from django.test import TestCase
from survey.home_data.home_score import HomeScore
from houseDatabase.models import RentDatabaseModel, ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel


class TestScoringMethods(TestCase):

    def setUp(self):
        self.home = RentDatabase.objects.create()

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

    def test_approx_commute_times_setter(self):
        # This test doesn't fit methodology and is probably bad
        home_score = HomeScore()
        self.assertEqual(home_score.approx_commute_times, [])
        home_score.approx_commute_times = 5
        home_score.approx_commute_times = 10
        self.assertEqual(home_score.approx_commute_times, [5,10])
        home_score.approx_commute_times = [1,2,3]
        self.assertEqual(home_score.approx_commute_times, [1,2,3])
        home_score.approx_commute_times = []
        self.assertEqual(home_score.approx_commute_times, [])

class TestApproxCommute(TestCase):

    def setUp(self):
        self.zip_code = "12345"
        self.zip_code1 = "01234"
        self.zip_code2 = "23456"
        self.commute_time = 6000 
        self.commute_distance = 700
        self.commute_type = "driving"

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

    def test_compute_approx_commute_times(self):
        # Arrange
        home_score=HomeScore()
        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)
        child_zip_code = self.create_code_dictionary_child(parent_zip_code, self.zip_code1, self.commute_time, 
                                                            self.commute_distance, self.commute_type)

        # Act
        ret1 = home_score.calculate_approx_commute(self.zip_code, self.zip_code1, self.commute_type)
        ret2 = home_score.calculate_approx_commute(self.zip_code, self.zip_code2, self.commute_type)
        ret3 = home_score.calculate_approx_commute("00000", self.zip_code, self.commute_type)

        # Assert

        self.assertEqual(ret1, [0, self.zip_code, self.zip_code1])
        self.assertEqual(home_score.approx_commute_times_minutes, [100])
        self.assertEqual(ret2, [1, self.zip_code, self.zip_code2])
        self.assertEqual(ret3, [1, "00000", self.zip_code])



