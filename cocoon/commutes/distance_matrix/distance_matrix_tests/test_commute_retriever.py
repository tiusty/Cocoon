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
        # Arrange
        commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)

        # Act
        retrieve_exact_commute([], [], commute_driving)

        # Assert
        # DistanceWrapper.get_durations_and_distances.assert_called_with()
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.DRIVING)

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_transit(self, mock_os):
        # Arrange
        commute_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)

        # Act
        retrieve_exact_commute([], [], commute_transit)

        # Assert
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.TRANSIT)

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_bicycling(self, mock_os):
        # Arrange
        commute_bike = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)

        # Act
        retrieve_exact_commute([], [], commute_bike)

        # Assert
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.BICYCLING)

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_walking(self, mock_os):
        # Arrange
        commute_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)

        # Act
        retrieve_exact_commute([], [], commute_walking)

        # Assert
        mock_os.assert_called_once_with([], [], mode=GoogleCommuteNaming.WALKING)
