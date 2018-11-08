from django.test import TestCase
from cocoon.scheduler.clientScheduler.client_scheduler import ClientScheduler
from unittest.mock import MagicMock

# import distance matrix wrapper
from cocoon.commutes.distance_matrix import commute_retriever

class TestClientScheduler(TestCase):

    def setUp(self):
        self.clientScheduler = ClientScheduler()

    '''
    def test_build_home_matrix_empty(self):
        homes_list = []
        commute_retriever.retrieve_exact_commute = MagicMock(returnValue=[(0,0), (0,1), (0,2)])
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        self.assertTrue(len(homes_matrix) == 0)

    def test_build_home_matrix_empty(self):
        homes_list = ["home1", "home2", "home3"]
        commute_retriever.retrieve_exact_commute = MagicMock(returnValue=[[(0,0), (0,1), (0,1)]])
        homes_matrix = self.clientScheduler.build_homes_matrix(homes_list)
        print(homes_matrix)

    '''
