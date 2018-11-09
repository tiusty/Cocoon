from django.test import TestCase
from cocoon.scheduler.clientScheduler.client_scheduler import ClientScheduler
from unittest.mock import MagicMock
from unittest.mock import patch

# import distance matrix wrapper
from cocoon.commutes.distance_matrix.commute_retriever import retrieve_exact_commute

class TestClientScheduler(TestCase):
    '''
    def setUp(self):
        self.clientScheduler = ClientScheduler()

    def test_build_home_matrix_empty(self, mock_commute):
        homes_list = []
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        self.assertTrue(len(homes_matrix) == 0)

    @patch('cocoon.scheduler.clientScheduler.client_scheduler.retrieve_exact_commute')
    def test_build_home_matrix_empty(self, mock_commute):
        homes_list = ["home1", "home2", "home3"]
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        print(homes_matrix)
    '''

