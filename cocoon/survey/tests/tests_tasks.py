# Import Django Modules
from django.test import TestCase

# Import mock
from unittest.mock import patch

from ..models import RentingSurveyModel
from ..tasks import notify_user_survey_updates
from cocoon.survey.cocoon_algorithm.rent_algorithm import RentAlgorithm
from cocoon.houseDatabase.models import HomeTypeModel, RentDatabaseModel, HomeProviderModel
from cocoon.userAuth.models import MyUser


class TestNofityUserSurveyUpdates(TestCase):

    @patch('cocoon.survey.tasks.email_user')
    def test_one_survey_needs_updates(self, mock_os):
        # Arrange
        user = MyUser.objects.create(email="test@test.com")
        listing_provider = HomeProviderModel.objects.get_or_create(provider=HomeProviderModel.MLSPIN)[0]
        home_type = HomeTypeModel.objects.get_or_create(home_type=HomeTypeModel.APARTMENT)[0]
        num_bedrooms = 2
        home = RentDatabaseModel.create_house_database(listing_provider=listing_provider,
                                                       home_type=home_type,
                                                       currently_available=True,
                                                       price=1500,
                                                       num_bedrooms=num_bedrooms, )
        home1 = RentDatabaseModel.create_house_database(listing_provider=listing_provider,
                                                        home_type=home_type,
                                                        currently_available=True,
                                                        price=2000,
                                                        num_bedrooms=num_bedrooms)
        survey = RentingSurveyModel.create_survey(user.userProfile,
                                                  max_price=2000,
                                                  desired_price=1500,
                                                  num_bedrooms=[num_bedrooms],
                                                  home_type=home_type,
                                                  wants_update=True,
                                                  price_weight=3,
                                                  update_frequency=0,
                                                  move_weight=3,
                                                  score_threshold=100,
                                                  num_home_threshold=1)

        # Act
        notify_user_survey_updates()

        # Assert
        mock_os.assert_called_once_with()




