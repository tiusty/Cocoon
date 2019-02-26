# Import Django Modules
from django.test import TestCase

# Import mock
from unittest.mock import patch, call

from ..models import RentingSurveyModel
from ..tasks import notify_user_survey_updates
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.userAuth.models import MyUser
from cocoon.survey.home_data.home_score import HomeScore


class TestNofityUserSurveyUpdates(TestCase):

    @patch('cocoon.survey.tasks.RentAlgorithm')
    @patch('cocoon.survey.tasks.email_user')
    def test_one_survey_needs_updates(self, mock_os, mock_alog):
        """
        Tests that if at least one home has past the score threshold and the survey update timestamp
            is valid, then the survey updates and calls the email function
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
        survey = RentingSurveyModel.create_survey(user.userProfile,
                                                  home_type=home_type,
                                                  wants_update=True,
                                                  update_frequency=0,
                                                  score_threshold=100,
                                                  num_home_threshold=1)

        # Create homes that will return from the algorithm
        home = HomeScore()
        home.accumulated_points = 100
        home.total_possible_points = 100

        home1 = HomeScore()
        home1.accumulated_points = 50
        home1.total_possible_points = 100

        mc = mock_alog.return_value
        mc.homes = [home, home1]

        # Act
        notify_user_survey_updates()

        # Assert
        mock_os.assert_called_once_with(survey)

    @patch('cocoon.survey.tasks.RentAlgorithm')
    @patch('cocoon.survey.tasks.email_user')
    def test_one_survey_needs_updates_no_homes_valid(self, mock_os, mock_alog):
        """
        Tests that if a survey needs updating but there isn't enough homes that meet
            the criteria then the email is not called
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
        survey = RentingSurveyModel.create_survey(user.userProfile,
                                                  home_type=home_type,
                                                  wants_update=True,
                                                  update_frequency=0,
                                                  score_threshold=100,
                                                  num_home_threshold=3)

        # Create homes that will return from the algorithm
        home = HomeScore()
        home.accumulated_points = 100
        home.total_possible_points = 100

        home1 = HomeScore()
        home1.accumulated_points = 50
        home1.total_possible_points = 100

        mc = mock_alog.return_value
        mc.homes = [home, home1]

        # Act
        notify_user_survey_updates()

        # Assert
        mock_os.assert_not_called()

    @patch('cocoon.survey.tasks.RentAlgorithm')
    @patch('cocoon.survey.tasks.email_user')
    def test_survey_marked_for_no_update(self, mock_os, mock_alog):
        """
        Tests that if the user marks to not update the survey then the survey is not updated
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
        survey = RentingSurveyModel.create_survey(user.userProfile,
                                                  home_type=home_type,
                                                  wants_update=False,
                                                  update_frequency=0,
                                                  score_threshold=100,
                                                  num_home_threshold=1)

        # Create homes that will return from the algorithm
        home = HomeScore()
        home.accumulated_points = 100
        home.total_possible_points = 100

        home1 = HomeScore()
        home1.accumulated_points = 50
        home1.total_possible_points = 100

        mc = mock_alog.return_value
        mc.homes = [home, home1]

        # Act
        notify_user_survey_updates()

        # Assert
        mock_os.assert_not_called()

    @patch('cocoon.survey.tasks.RentAlgorithm')
    @patch('cocoon.survey.tasks.email_user')
    def test_multiple_surveys_all_need_updating(self, mock_os, mock_alog):
        """
        Tests that if multiple surveys need to be updated, then it updates
            all of them
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
        survey = RentingSurveyModel.create_survey(user.userProfile,
                                                  home_type=home_type,
                                                  wants_update=True,
                                                  update_frequency=0,
                                                  score_threshold=100,
                                                  num_home_threshold=1)

        survey1 = RentingSurveyModel.create_survey(user.userProfile,
                                                  home_type=home_type,
                                                  wants_update=True,
                                                  update_frequency=0,
                                                  score_threshold=100,
                                                  num_home_threshold=1)

        # Create homes that will return from the algorithm
        home = HomeScore()
        home.accumulated_points = 100
        home.total_possible_points = 100

        home1 = HomeScore()
        home1.accumulated_points = 50
        home1.total_possible_points = 100

        mc = mock_alog.return_value
        mc.homes = [home, home1]

        # Act
        notify_user_survey_updates()

        # Assert
        mock_os.assert_has_calls(
            [
                call(survey),
                call(survey1)
            ]

        )

    @patch('cocoon.survey.tasks.RentAlgorithm')
    @patch('cocoon.survey.tasks.email_user')
    def test_multiple_surveys_one_wants_updating(self, mock_os, mock_alog):
        """
        Tests that if there are multiple surveys but one is marked as want update,
            then only that survey gets updated
        """
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
        survey = RentingSurveyModel.create_survey(user.userProfile,
                                                  home_type=home_type,
                                                  wants_update=False,
                                                  update_frequency=0,
                                                  score_threshold=100,
                                                  num_home_threshold=1)

        survey1 = RentingSurveyModel.create_survey(user.userProfile,
                                                   home_type=home_type,
                                                   wants_update=True,
                                                   update_frequency=0,
                                                   score_threshold=100,
                                                   num_home_threshold=1)

        # Create homes that will return from the algorithm
        home = HomeScore()
        home.accumulated_points = 100
        home.total_possible_points = 100

        home1 = HomeScore()
        home1.accumulated_points = 50
        home1.total_possible_points = 100

        mc = mock_alog.return_value
        mc.homes = [home, home1]

        # Act
        notify_user_survey_updates()

        # Assert
        mock_os.assert_has_calls(
            [
                call(survey1)
            ]

        )







