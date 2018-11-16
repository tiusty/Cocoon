# Import Django Unittest library
from django.test import TestCase

# Import python libraries
from unittest.mock import MagicMock

# Import Commute modules
from cocoon.commutes.models import ZipCodeBase
from cocoon.commutes.constants import CommuteAccuracy

# Import Distance matrix classes
from cocoon.commutes.distance_matrix.commute_cache_updater import Driving, Transit, Bicycling, Walking, \
    update_commutes_cache

# Import home score
from cocoon.survey.home_data.home_score import HomeScore

# Import Destination model
from cocoon.survey.models import RentingSurveyModel, HomeTypeModel, CommuteType, HomeProviderModel

# Import houseDatabase object
from cocoon.houseDatabase.models import RentDatabaseModel

# Import Users
from cocoon.userAuth.models import MyUser


class TestUpdateCommutesCache(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    def test_one_destination_driving(self):
        """
        Tests to make sure if the destination selects driving, that driving is actually selected
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_type)
        accuracy = CommuteAccuracy.EXACT

        Driving.run = MagicMock()
        Transit.run = MagicMock()
        Bicycling.run = MagicMock()
        Walking.run = MagicMock()

        # Act
        update_commutes_cache([home_score], [destination], accuracy=accuracy)

        # Assert
        Driving.run.assert_called_once_with()
        Transit.run.assert_not_called()
        Bicycling.run.assert_not_called()
        Walking.run.assert_not_called()

    def test_one_destination_transit(self):
        """
        Tests to make sure if the destination selects transit, that transit is actually selected
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_type)
        accuracy = CommuteAccuracy.EXACT

        Driving.run = MagicMock()
        Transit.run = MagicMock()
        Bicycling.run = MagicMock()
        Walking.run = MagicMock()

        # Act
        update_commutes_cache([home_score], [destination], accuracy=accuracy)

        # Assert
        Driving.run.assert_not_called()
        Transit.run.assert_called_once_with()
        Bicycling.run.assert_not_called()
        Walking.run.assert_not_called()

    def test_one_destination_bicycling(self):
        """
        Tests to make sure if the destination selects bicycling, that bicycling is actually selected
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_type)
        accuracy = CommuteAccuracy.EXACT

        Driving.run = MagicMock()
        Transit.run = MagicMock()
        Bicycling.run = MagicMock()
        Walking.run = MagicMock()

        # Act
        update_commutes_cache([home_score], [destination], accuracy=accuracy)

        # Assert
        Driving.run.assert_not_called()
        Transit.run.assert_not_called()
        Bicycling.run.assert_called_once_with()
        Walking.run.assert_not_called()

    def test_one_destination_walking(self):
        """
        Tests to make sure if the destination selects walking, that waking is actually selected
        """
        # Arrange
        commute_type = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_type)
        accuracy = CommuteAccuracy.EXACT

        Driving.run = MagicMock()
        Transit.run = MagicMock()
        Bicycling.run = MagicMock()
        Walking.run = MagicMock()

        # Act
        update_commutes_cache([home_score], [destination], accuracy=accuracy)

        # Assert
        Driving.run.assert_not_called()
        Transit.run.assert_not_called()
        Bicycling.run.assert_not_called()
        Walking.run.assert_called_once_with()

    def test_three_destination_driving_transit_bicycling_walking(self):
        """
        Tests to make sure if multiple destinations are inputed then it loops and selectes
            the appropriate functions
        """
        # Arrange
        commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        commute_transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)
        commute_walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        commute_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type)
        destination = self.create_destination(survey, commute_type=commute_driving)
        destination1 = self.create_destination(survey, commute_type=commute_walking)
        destination2 = self.create_destination(survey, commute_type=commute_bicycling)
        destination3 = self.create_destination(survey, commute_type=commute_transit)
        accuracy = CommuteAccuracy.EXACT

        Driving.run = MagicMock()
        Transit.run = MagicMock()
        Bicycling.run = MagicMock()
        Walking.run = MagicMock()

        # Act
        update_commutes_cache([home_score], [destination, destination1, destination2, destination3], accuracy=accuracy)

        # Assert
        Driving.run.assert_called_once_with()
        Transit.run.assert_called_once_with()
        Bicycling.run.assert_called_once_with()
        Walking.run.assert_called_once_with()


class TestDriveCommuteCalculator(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        self.commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        self.commute_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN")
        ))

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    def test_find_missing_pairs_all_exist_all_same_commute(self):
        """
        Tests that if all the zipcodes pair exist for that commute then there is no failed homes
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_driving)
        parent_zip.zipcodechild_set.create(zip_code='02475', commute_type=self.commute_driving)
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=self.commute_driving)

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, set())

    def test_find_missing_pairs_some_exist_all_same_commute(self):
        """
        Tests that if some of the pairs do not exist, then those homes show up in the failed list
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_driving)

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score1.home.zip_code, home_score1.home.state)})

    def test_find_missing_pairs_some_exist_all_different_commutes(self):
        """
        Tests that if some of the pairs exist in a different commute type then those homes should
            show up in the failed homes
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=self.commute_driving)
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_bicycling)
        parent_zip.zipcodechild_set.create(zip_code='02475', commute_type=self.commute_bicycling)

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score1.home.zip_code, home_score1.home.state),
                                  (home_score2.home.zip_code, home_score2.home.state)})

    def test_find_missing_pairs_none_exist(self):
        """
        Tests that if none of the pairs exist then all of them are in the failed homes list
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        ZipCodeBase.objects.create(zip_code='02476')

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score1.home.zip_code, home_score1.home.state),
                                  (home_score2.home.zip_code, home_score2.home.state)})

    def test_find_missing_pairs_parent_zip_code_does_not_exist(self):
        """
        Tests that if the parent zip_code object doesn't exist then all the homes are added to the
            failed list
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        home_score3 = self.create_home(self.home_type, zip_code='02111')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        # Act
        homes = [home_score, home_score1, home_score2, home_score3]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score1.home.zip_code, home_score1.home.state),
                                  (home_score2.home.zip_code, home_score2.home.state),
                                  (home_score3.home.zip_code, home_score3.home.state)})

    def test_find_missing_pairs_no_duplicates_in_failed_list(self):
        """
        Tests that if there are multiple failed homes with the same zip_code then make sure
            they aren't duplicated
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02476')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        home_score3 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        ZipCodeBase.objects.create(zip_code='02476')

        # Act
        homes = [home_score, home_score1, home_score2, home_score3]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score3.home.zip_code, home_score3.home.state)})

    def test_run_approximate(self):
        """
        Tests to make sure that the check_all_combinations is called when approximate commutes are desired. It also
            makes sure that the run_exact_commute_cache function is not called
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02474')

        commute_calculator = Driving([home_score], destination, accuracy=CommuteAccuracy.APPROXIMATE)

        Driving.check_all_combinations = MagicMock()
        Driving.run_exact_commute_cache = MagicMock()

        # Act
        commute_calculator.run()

        # Assert
        Driving.check_all_combinations.assert_called_once_with()
        Driving.run_exact_commute_cache.assert_not_called()

    def test_run_exact(self):
        """
        Tests to make sure that the run_exact_commute is called when exact commutes are desired. It also makes
            sure that the check_all_combinations is not called
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02474')

        commute_calculator = Driving([home_score], destination, accuracy=CommuteAccuracy.EXACT)

        Driving.check_all_combinations = MagicMock()
        Driving.run_exact_commute_cache = MagicMock()

        # Act
        commute_calculator.run()

        # Assert
        Driving.run_exact_commute_cache.assert_called_once_with()
        Driving.check_all_combinations.assert_not_called()


class TestTransitCommuteCalculator(TestCase):
    """
    Currently the Transit option is supposed to be exactly the same as Driving. Therefore,
        the unit tests are copied over with the Driving options switched to Transit.
        Later switch the unit tests to the desired functionality
    """

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type='House')
        self.commute_driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        self.commute_bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        HomeProviderModel.objects.create(provider="MLSPIN")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=HomeProviderModel.objects.get(provider="MLSPIN"),
        ))

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.tenants.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    def test_find_missing_pairs_all_exist_all_same_commute(self):
        """
        Tests that if all the zipcodes pair exist for that commute then there is no failed homes
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_driving)
        parent_zip.zipcodechild_set.create(zip_code='02475', commute_type=self.commute_driving)
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=self.commute_driving)

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, set())

    def test_find_missing_pairs_some_exist_all_same_commute(self):
        """
        Tests that if some of the pairs do not exist, then those homes show up in the failed list
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_driving)

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score1.home.zip_code, home_score1.home.state)})

    def test_find_missing_pairs_some_exist_all_different_commutes(self):
        """
        Tests that if some of the pairs exist in a different commute type then those homes should
            show up in the failed homes
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02476', commute_type=self.commute_driving)
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_bicycling)
        parent_zip.zipcodechild_set.create(zip_code='02475', commute_type=self.commute_bicycling)

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score1.home.zip_code, home_score1.home.state),
                                  (home_score2.home.zip_code, home_score2.home.state)})

    def test_find_missing_pairs_none_exist(self):
        """
        Tests that if none of the pairs exist then all of them are in the failed homes list
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        ZipCodeBase.objects.create(zip_code='02476')

        # Act
        homes = [home_score, home_score1, home_score2]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score1.home.zip_code, home_score1.home.state),
                                  (home_score2.home.zip_code, home_score2.home.state)})

    def test_find_missing_pairs_parent_zip_code_does_not_exist(self):
        """
        Tests that if the parent zip_code object doesn't exist then all the homes are added to the
            failed list
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02475')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        home_score3 = self.create_home(self.home_type, zip_code='02111')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        # Act
        homes = [home_score, home_score1, home_score2, home_score3]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score1.home.zip_code, home_score1.home.state),
                                  (home_score2.home.zip_code, home_score2.home.state),
                                  (home_score3.home.zip_code, home_score3.home.state)})

    def test_find_missing_pairs_no_duplicates_in_failed_list(self):
        """
        Tests that if there are multiple failed homes with the same zip_code then make sure
            they aren't duplicated
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        home_score1 = self.create_home(self.home_type, zip_code='02476')
        home_score2 = self.create_home(self.home_type, zip_code='02474')
        home_score3 = self.create_home(self.home_type, zip_code='02474')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02476')

        commute_calculator = Driving([home_score], destination)

        ZipCodeBase.objects.create(zip_code='02476')

        # Act
        homes = [home_score, home_score1, home_score2, home_score3]
        result = commute_calculator.find_missing_pairs(homes)

        # Assert
        self.assertEqual(result, {(home_score.home.zip_code, home_score.home.state),
                                  (home_score3.home.zip_code, home_score3.home.state)})

    def test_run_approximate(self):
        """
        Tests to make sure that the check_all_combinations is called when approximate commutes are desired. It also
            makes sure that the run_exact_commute_cache function is not called
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02474')

        commute_calculator = Transit([home_score], destination, accuracy=CommuteAccuracy.APPROXIMATE)

        Transit.check_all_combinations = MagicMock()
        Transit.run_exact_commute_cache = MagicMock()

        # Act
        commute_calculator.run()

        # Assert
        Transit.check_all_combinations.assert_called_once_with()
        Transit.run_exact_commute_cache.assert_not_called()

    def test_run_exact(self):
        """
        Tests to make sure that the run_exact_commute is called when exact commutes are desired. It also makes
            sure that the check_all_combinations is not called
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_driving, zip_code='02474')

        commute_calculator = Transit([home_score], destination, accuracy=CommuteAccuracy.EXACT)

        Transit.check_all_combinations = MagicMock()
        Transit.run_exact_commute_cache = MagicMock()

        # Act
        commute_calculator.run()

        # Assert
        Transit.run_exact_commute_cache.assert_called_once_with()
        Transit.check_all_combinations.assert_not_called()
