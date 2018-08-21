from django.test import TestCase
from cocoon.survey.home_data.home_score import HomeScore
from cocoon.userAuth.models import MyUser
from cocoon.survey.models import RentingDestinationsModel, RentingSurveyModel
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel
from cocoon.commutes.models import ZipCodeBase, CommuteType


class TestScoringMethods(TestCase):

    def setUp(self):
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = RentDatabaseModel.objects.create(home_type_home=self.home_type)

    def test_percent_score_positive(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual((accumulated_points/total_possible_points) * 100, home_score.percent_score())

    def test_percent_score_positive_eliminated(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_negative(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = -20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_negative_eliminated(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = -20
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_negative(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = -30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_negative_eliminated(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = -30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_accumulated_points_zero(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 0
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(0, home_score.percent_score())

    def test_percent_score_accumulated_points_zero_eliminated(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 0
        total_possible_points = 30

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_percent_score_total_possible_points_zero(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 30
        total_possible_points = 0

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(0, home_score.percent_score())

    def test_percent_score_total_possible_points_zero_eliminated(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 30
        total_possible_points = 0

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points
        home_score.eliminate_home()

        # Assert
        self.assertEqual(-1, home_score.percent_score())

    def test_eliminate_home(self):
        # Arrange // not really following methodology
        home_score = HomeScore()
        self.assertFalse(home_score.eliminated)
        home_score.eliminate_home()
        self.assertTrue(home_score.eliminated)

    def test_user_friendly_score(self):
        # Arrange
        home_score = HomeScore()
        accumulated_points = 20
        total_possible_points = 50

        # Act
        home_score._accumulated_points = accumulated_points
        home_score._total_possible_points = total_possible_points

        # Assert
        self.assertEqual(round((accumulated_points/total_possible_points)*100), home_score.user_friendly_score())

    def test_home_setter_constructor(self):
        # Arrange
        home_score = HomeScore(self.home)

        # Assert
        self.assertIsNotNone(home_score.home)

    def test_home_setter_later(self):
        # Arrange // Note really following methodology
        home_score = HomeScore()
        self.assertIsNone(home_score.home)
        home_score.home = self.home
        self.assertIsNotNone(home_score.home)

    def test_approx_commute_times_setter_basic(self):
        # Arrange
        home_score = HomeScore()
        self.assertEqual(home_score.approx_commute_times, {})

        # Act
        home_score.approx_commute_times = {"12345": 10}
        home_score.approx_commute_times = {"01234": 20}

        # Assert
        self.assertEqual(home_score.approx_commute_times, {"12345": 10, "01234": 20})

    def test_approx_commute_times_setter_overwriting(self):
        # Arrange
        home_score = HomeScore()
        self.assertEqual(home_score.approx_commute_times, {})

        # Act
        home_score.approx_commute_times = {"12345": 10}
        home_score.approx_commute_times = {"01234": 20}
        home_score.approx_commute_times = {}
        home_score.approx_commute_times = {"12345": 50}

        # Assert
        self.assertEqual(home_score.approx_commute_times, {"12345": 50, "01234": 20})


class TestApproxCommute(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(email="test@email.com")
        self.zip_code = "12345"
        self.zip_code1 = "01234"
        self.zip_code2 = "23456"
        self.commute_time = 6000 
        self.commute_distance = 700
        self.commute_type = CommuteType.objects.create(commute_type='Driving')
        self.commute_type_walking = CommuteType.objects.create(commute_type='Walking')

    @staticmethod
    def create_survey(user_profile, max_price=1500, min_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2):
        return RentingSurveyModel.objects.create(
            user_profile_survey=user_profile,
            max_price_survey=max_price,
            min_price_survey=min_price,
            max_bathrooms_survey=max_bathroom,
            min_bathrooms_survey=min_bathroom,
            num_bedrooms_survey=num_bedrooms,
        )

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

    @staticmethod
    def create_zip_code_dictionary(zip_code):
        return ZipCodeBase.objects.create(zip_code=zip_code)

    @staticmethod
    def create_zip_code_dictionary_child(parent_zip_code_dictionary, zip_code, commute_time, 
                                         commute_distance, commute_type):
        parent_zip_code_dictionary.zipcodechild_set.create(
                zip_code=zip_code,
                commute_time_seconds=commute_time,
                commute_distance_meters=commute_distance,
                commute_type=commute_type,
                )

    def test_populate_approx_commute_times(self):
        # Arrange
        survey = self.create_survey(self.user.userProfile)
        home_score = HomeScore()

        self.zip_code = "12345"
        self.zip_code1 = "01234"
        self.zip_code2 = "23456"

        destination = self.create_destination(survey, self.commute_type, street_address="101 Test Street",
                                              city="Los Angeles", state="California", zip_code=self.zip_code1)
        destination1 = self.create_destination(survey, self.commute_type, street_address="101 Test Street",
                                               city="Los Angeles", state="California", zip_code=self.zip_code2)
        destination2 = self.create_destination(survey, self.commute_type, street_address="101 Test Street",
                                               city="Los Angeles", state="California", zip_code=self.zip_code)

        parent_zip_code = self.create_zip_code_dictionary(self.zip_code)
        self.create_zip_code_dictionary_child(parent_zip_code, self.zip_code1, self.commute_time,
                                              self.commute_distance, self.commute_type)

        # Act
        ret1 = home_score.populate_approx_commutes(self.zip_code, destination, self.commute_type)
        ret2 = home_score.populate_approx_commutes(self.zip_code, destination1, self.commute_type)
        ret3 = home_score.populate_approx_commutes("00000", destination, self.commute_type)
        ret4 = home_score.populate_approx_commutes(self.zip_code, destination2, self.commute_type_walking)

        # Assert
        self.assertEqual(ret1, True)
        self.assertEqual(home_score.approx_commute_times, {destination: 100.0})
        self.assertEqual(ret2, False)
        self.assertEqual(ret3, False)
        self.assertEqual(ret4, False)