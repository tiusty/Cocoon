import unittest
from survey.home_data.home_score import HomeScore


class TestScoringMethods(unittest.TestCase):

    def test_percent_score_positive(self):
        home = HomeScore()
        accumulated_points = 20
        total_possible_points = 30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual((accumulated_points/total_possible_points) * 100, home.percent_score())

    def test_percent_score_positive_eliminated(self):
        home = HomeScore()
        accumulated_points = 20
        total_possible_points = 30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        home.eliminate_home()
        self.assertEqual(-1, home.percent_score())

    def test_percent_score_accumulated_points_negative(self):
        home = HomeScore()
        accumulated_points = -20
        total_possible_points = 30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual(-1, home.percent_score())

    def test_percent_score_accumulated_points_negative_eliminated(self):
        home = HomeScore()
        accumulated_points = -20
        total_possible_points = 30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        home.eliminate_home()
        self.assertEqual(-1, home.percent_score())

    def test_percent_score_total_possible_points_negative(self):
        home = HomeScore()
        accumulated_points = 20
        total_possible_points = -30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual(-1, home.percent_score())

    def test_percent_score_total_possible_points_negative_eliminated(self):
        home = HomeScore()
        accumulated_points = 20
        total_possible_points = -30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        home.eliminate_home()
        self.assertEqual(-1, home.percent_score())

    def test_percent_score_accumulated_points_zero(self):
        home = HomeScore()
        accumulated_points = 0
        total_possible_points = 30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual(0, home.percent_score())

    def test_percent_score_accumulated_points_zero_eliminated(self):
        home = HomeScore()
        accumulated_points = 0
        total_possible_points = 30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        home.eliminate_home()
        self.assertEqual(-1, home.percent_score())

    def test_percent_score_total_possible_points_zero(self):
        home = HomeScore()
        accumulated_points = 30
        total_possible_points = 0
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual(0, home.percent_score())

    def test_percent_score_total_possible_points_zero_eliminated(self):
        home = HomeScore()
        accumulated_points = 30
        total_possible_points = 0
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        home.eliminate_home()
        self.assertEqual(-1, home.percent_score())

    def test_eliminate_home(self):
        home = HomeScore()
        self.assertFalse(home.eliminated)
        home.eliminate_home()
        self.assertTrue(home.eliminated)

    def test_user_friendly_score(self):
        home = HomeScore()
        accumulated_points = 20
        total_possible_points = 50
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual(round((accumulated_points/total_possible_points)*100), home.user_friendly_score())
