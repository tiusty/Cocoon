# Import Django Modules
from django.test import TestCase

# Import third party libraries
from unittest.mock import patch

# Retrieve Cocoon Modules
from cocoon.commutes.distance_matrix.commute_retriever import retrieve_exact_commute
from cocoon.commutes.models import CommuteType

# Retrieve Cocoon Constants
from cocoon.commutes.constants import GoogleCommuteNaming


class TestRetrieveExactCommute(TestCase):

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_driving(self, mock_os):
        # Act
        retrieve_exact_commute([], [], mode=CommuteType.DRIVING)

        # Assert
        # DistanceWrapper.get_durations_and_distances.assert_called_with()
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.DRIVING)

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_transit(self, mock_os):
        # Act
        retrieve_exact_commute([], [], mode=CommuteType.TRANSIT)

        # Assert
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.TRANSIT)

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_bicycling(self, mock_os):
        # Act
        retrieve_exact_commute([], [], mode=CommuteType.BICYCLING)

        # Assert
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.BICYCLING)

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_walking(self, mock_os):
        # Act
        retrieve_exact_commute([], [], mode=CommuteType.WALKING)

        # Assert
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.WALKING)
