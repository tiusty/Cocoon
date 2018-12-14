# Import Django Modules
from django.test import TestCase

# Import third party libraries
from unittest.mock import patch

# Retrieve Cocoon Modules
from ..commute_retriever import retrieve_exact_commute, retrieve_approximate_commute
from ...models import CommuteType, ZipCodeBase, ZipCodeChild
from ..home_commute import HomeCommute

# Retrieve Cocoon Constants
from ...constants import GoogleCommuteNaming


class TestRetrieveExactCommute(TestCase):

    @patch('cocoon.commutes.distance_matrix.commute_retriever.DistanceWrapper.get_durations_and_distances')
    def test_mode_driving(self, mock_os):
        # Arrange
        commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)

        # Act
        retrieve_exact_commute([], [], commute_driving)

        # Assert
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


class TestApproximateCommute(TestCase):

    def test_driving_working(self):
        """
        Test a simple working case with driving
        """
        # Arrange
        commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)

        home = HomeCommute('02476', 'MA')
        home1 = HomeCommute('02474', 'MA')
        homes = [home, home1]
        destination = HomeCommute('02476', 'MA')

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=commute_driving, commute_time_seconds=60)
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=commute_driving, commute_time_seconds=120)

        # Act
        result = retrieve_approximate_commute(homes, destination, CommuteType.DRIVING)

        # Assert
        self.assertEqual(result, [120, 60])

    def test_transit_working(self):
        """
        Test a simple working case with transit
        """
        # Arrange
        commute_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)

        home = HomeCommute('02476', 'MA')
        home1 = HomeCommute('02474', 'MA')
        homes = [home, home1]
        destination = HomeCommute('02476', 'MA')

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=commute_transit, commute_time_seconds=60)
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=commute_transit, commute_time_seconds=120)

        # Act
        result = retrieve_approximate_commute(homes, destination, CommuteType.TRANSIT)

        # Assert
        self.assertEqual(result, [120, 60])

    def test_one_driving_one_transit(self):
        """
        Test a case where one commute is driving and one is transit so for the home that
            had a transit commute it returns -1 since the distance doesn't exist
        """
        # Arrange
        commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        commute_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)

        home = HomeCommute('02476', 'MA')
        home1 = HomeCommute('02474', 'MA')
        homes = [home, home1]
        destination = HomeCommute('02476', 'MA')

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=commute_driving, commute_time_seconds=60)
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=commute_transit, commute_time_seconds=120)

        # Act
        result = retrieve_approximate_commute(homes, destination, CommuteType.DRIVING)

        # Assert
        self.assertEqual(result, [-1, 60])

    def test_none_exist(self):
        """
        Tests that none of the combinations exist so both homes return -1
        """
        # Arrange
        commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        commute_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)

        home = HomeCommute('02473', 'MA')
        home1 = HomeCommute('02472', 'MA')
        homes = [home, home1]
        destination = HomeCommute('02476', 'MA')

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=commute_driving, commute_time_seconds=60)
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=commute_transit, commute_time_seconds=120)

        # Act
        result = retrieve_approximate_commute(homes, destination, CommuteType.DRIVING)

        # Assert
        self.assertEqual(result, [-1, -1])

    def test_zip_base_does_not_exist(self):
        """
        Tests that if the zip code base doesn't exist then all -1's are returned
        """
        # Arrange
        home = HomeCommute('02473', 'MA')
        home1 = HomeCommute('02472', 'MA')
        home2 = HomeCommute('02473', 'MA')
        homes = [home, home1, home2]
        destination = HomeCommute('02476', 'MA')

        # Act
        result = retrieve_approximate_commute(homes, destination, CommuteType.DRIVING)

        # Assert
        self.assertEqual(result, [-1, -1, -1])
