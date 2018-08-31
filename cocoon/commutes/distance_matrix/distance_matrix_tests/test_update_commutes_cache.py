# Import Django Unittest library
from django.test import TestCase

# Import django libraries
from django.utils import timezone

# Import python libraries
from unittest.mock import MagicMock

# Import Commute modules
from cocoon.commutes.models import ZipCodeBase
from cocoon.commutes.constants import ZIP_CODE_TIMEDELTA_VALUE, CommuteAccuracy, GoogleCommuteNaming

# Import Distance matrix classes
from cocoon.commutes.distance_matrix.commute_cache_updater import Driving, Transit, Bicycling, Walking, \
    update_commutes_cache

# Import home score
from cocoon.survey.home_data.home_score import HomeScore

# Import Destination model
from cocoon.survey.models import RentingSurveyModel, HomeTypeModel, CommuteType

# Import houseDatabase object
from cocoon.houseDatabase.models import RentDatabaseModel

# Import Users
from cocoon.userAuth.models import MyUser


class TestUpdateCommutesCache(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile_survey=user_profile,
            max_price_survey=max_price,
            desired_price_survey=desired_price,
            max_bathrooms_survey=max_bathroom,
            min_bathrooms_survey=min_bathroom,
            num_bedrooms_survey=num_bedrooms,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type_home=home_type,
            price_home=price,
            currently_available_home=currently_available,
            num_bedrooms_home=num_bedrooms,
            num_bathrooms_home=num_bathrooms,
            zip_code_home=zip_code,
            state_home=state,
        ))

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.rentingdestinationsmodel_set.create(
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
        commute_type = CommuteType.objects.create(commute_type=GoogleCommuteNaming.DRIVING)
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
        commute_type = CommuteType.objects.create(commute_type=GoogleCommuteNaming.TRANSIT)
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
        commute_type = CommuteType.objects.create(commute_type=GoogleCommuteNaming.BICYCLING)
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
        commute_type = CommuteType.objects.create(commute_type=GoogleCommuteNaming.WALKING)
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
        commute_driving = CommuteType.objects.create(commute_type=GoogleCommuteNaming.DRIVING)
        commute_transit = CommuteType.objects.create(commute_type=GoogleCommuteNaming.TRANSIT)
        commute_walking = CommuteType.objects.create(commute_type=GoogleCommuteNaming.WALKING)
        commute_bicycling = CommuteType.objects.create(commute_type=GoogleCommuteNaming.BICYCLING)
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
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.commute_type = CommuteType.objects.create(commute_type='Driving')

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile_survey=user_profile,
            max_price_survey=max_price,
            desired_price_survey=desired_price,
            max_bathrooms_survey=max_bathroom,
            min_bathrooms_survey=min_bathroom,
            num_bedrooms_survey=num_bedrooms,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type_home=home_type,
            price_home=price,
            currently_available_home=currently_available,
            num_bedrooms_home=num_bedrooms,
            num_bathrooms_home=num_bathrooms,
            zip_code_home=zip_code,
            state_home=state,
        ))

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.rentingdestinationsmodel_set.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    def test_does_pair_exist_true(self):
        """
        Tests that if the zip code pair exists for the home and the destination, then the does_exist_pair
            function returns true
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

        commute_calculator = Driving([home_score], destination)
        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_type)

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertTrue(result)

    def test_does_pair_exist_false(self):
        """
        Tests that if the zip code pair exists for the home and the destination, then the does_exist_pair
            function returns true
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02475')

        commute_calculator = Driving([home_score], destination)
        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_type)

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertFalse(result)

    def test_zip_code_pair_exists_but_not_valid(self):
        """
        Tests that if the pair exists but is out of date, then the does pair exists will return false
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

        commute_calculator = Driving([home_score], destination)
        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_type,
                                           last_date_updated=timezone.now() -
                                           timezone.timedelta(days=ZIP_CODE_TIMEDELTA_VALUE + 1))

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertFalse(result)

    def test_zip_code_pair_no_zip_codes(self):
        """
        Tests that if there are no zip codes in the database, then the does pair exist will return false
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

        commute_calculator = Driving([home_score], destination)

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertFalse(result)

    def test_run_approximate(self):
        """
        Tests to make sure that the check_all_combinations is called when approximate commutes are desired. It also
            makes sure that the run_exact_commute_cache function is not called
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

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
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

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
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.commute_type = CommuteType.objects.create(commute_type='Transit')

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile_survey=user_profile,
            max_price_survey=max_price,
            desired_price_survey=desired_price,
            max_bathrooms_survey=max_bathroom,
            min_bathrooms_survey=min_bathroom,
            num_bedrooms_survey=num_bedrooms,
        )

    @staticmethod
    def create_home(home_type, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type_home=home_type,
            price_home=price,
            currently_available_home=currently_available,
            num_bedrooms_home=num_bedrooms,
            num_bathrooms_home=num_bathrooms,
            zip_code_home=zip_code,
            state_home=state,
        ))

    @staticmethod
    def create_destination(survey, commute_type, street_address="12 Stony Brook Rd", city="Arlington", state="MA",
                           zip_code="02476", commute_weight=0, max_commute=60, min_commute=0):
        return survey.rentingdestinationsmodel_set.create(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            commute_type=commute_type,
            commute_weight=commute_weight,
            max_commute=max_commute,
            min_commute=min_commute,
        )

    def test_does_pair_exist_true(self):
        """
        Tests that if the zip code pair exists for the home and the destination, then the does_exist_pair
            function returns true
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

        commute_calculator = Transit([home_score], destination)
        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_type)

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertTrue(result)

    def test_does_pair_exist_false(self):
        """
        Tests that if the zip code pair exists for the home and the destination, then the does_exist_pair
            function returns true
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02475')

        commute_calculator = Transit([home_score], destination)
        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_type)

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertFalse(result)

    def test_zip_code_pair_exists_but_not_valid(self):
        """
        Tests that if the pair exists but is out of date, then the does pair exists will return false
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

        commute_calculator = Transit([home_score], destination)
        parent_zip = ZipCodeBase.objects.create(zip_code='02476')
        parent_zip.zipcodechild_set.create(zip_code='02474', commute_type=self.commute_type,
                                           last_date_updated=timezone.now() -
                                                             timezone.timedelta(days=ZIP_CODE_TIMEDELTA_VALUE + 1))

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertFalse(result)

    def test_zip_code_pair_no_zip_codes(self):
        """
        Tests that if there are no zip codes in the database, then the does pair exist will return false
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

        commute_calculator = Transit([home_score], destination)

        # Act
        result = commute_calculator.does_pair_exist(home_score.home)

        # Assert
        self.assertFalse(result)

    def test_run_approximate(self):
        """
        Tests to make sure that the check_all_combinations is called when approximate commutes are desired. It also
            makes sure that the run_exact_commute_cache function is not called
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = self.create_home(self.home_type, zip_code='02476')
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

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
        destination = self.create_destination(survey, self.commute_type, zip_code='02474')

        commute_calculator = Transit([home_score], destination, accuracy=CommuteAccuracy.EXACT)

        Transit.check_all_combinations = MagicMock()
        Transit.run_exact_commute_cache = MagicMock()

        # Act
        commute_calculator.run()

        # Assert
        Transit.run_exact_commute_cache.assert_called_once_with()
        Transit.check_all_combinations.assert_not_called()
