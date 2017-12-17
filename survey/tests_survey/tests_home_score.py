import unittest
from survey.home_data.home_score import HomeScore


class TestScoringMethods(unittest.TestCase):

    def test_percent_score(self):
        home = HomeScore()
        accumulated_points = 20
        total_possible_points = 30
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual(home.percent_score(), (accumulated_points/total_possible_points) * 100)

    def test_user_friendly_score(self):
        home = HomeScore()
        accumulated_points = 20
        total_possible_points = 50
        home._accumulated_points = accumulated_points
        home._total_possible_points = total_possible_points
        self.assertEqual(home.user_friendly_score(), round((accumulated_points/total_possible_points)*100))
