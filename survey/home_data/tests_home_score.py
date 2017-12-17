from django.test import TestCase
from survey.home_data.home_score import HomeScore
from houseDatabase.models import RentDatabase


class TestScoringMethods(TestCase):

    def setUp(self):
        self.home = RentDatabase.objects.create()

    def test_percent_score_positive(self):
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = 30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        self.assertEqual((accumulated_points/total_possible_points) * 100, home_score.percent_score())

    def test_percent_score_positive_eliminated(self):
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = 30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_negative(self):
        home_score = HomeScore()
        accumulated_points = -20
        total_possible_points = 30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_negative_eliminated(self):
        home_score = HomeScore()
        accumulated_points = -20
        total_possible_points = 30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_negative(self):
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = -30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_negative_eliminated(self):
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = -30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_zero(self):
        home_score = HomeScore()
        accumulated_points = 0
        total_possible_points = 30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        self.assertEqual(0, home_score.percent_score())

    def test_percent_score_accumulated_points_zero_eliminated(self):
        home_score = HomeScore()
        accumulated_points = 0
        total_possible_points = 30
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_zero(self):
        home_score = HomeScore()
        accumulated_points = 30
        total_possible_points = 0
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        self.assertEqual(0, home_score.percent_score())

    def test_percent_score_total_possible_points_zero_eliminated(self):
        home_score = HomeScore()
        accumulated_points = 30
        total_possible_points = 0
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()
        self.assertEqual(-1, home_score.percent_score())

    def test_eliminate_home(self):
        home_score = HomeScore()
        self.assertFalse(home_score.eliminated)
        home_score.eliminate_home()
        self.assertTrue(home_score.eliminated)

    def test_user_friendly_score(self):
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = 50
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        self.assertEqual(round((accumulated_points/total_possible_points)*100), home_score.user_friendly_score())

    def test_home_setter_constructor(self):
        home_score = HomeScore(self.home)
        self.assertIsNotNone(home_score.home)

    def test_home_setter_later(self):
        home_score = HomeScore()
        self.assertIsNone(home_score.home)
        home_score.home = self.home
        self.assertIsNotNone(home_score.home)
