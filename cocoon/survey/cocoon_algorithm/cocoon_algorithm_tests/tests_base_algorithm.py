from django.test import TestCase
from django.utils import timezone

# Import Python Modules
from datetime import timedelta

# Cocoon modules
from cocoon.survey.models import RentingSurveyModel
from cocoon.userAuth.models import MyUser
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, HomeProviderModel
from cocoon.survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm
from cocoon.survey.home_data.home_score import HomeScore
from cocoon.survey.constants import DAYS_AFTER_MOVE_IN_ADDED, DAYS_BEFORE_MOVE_IN_ADDED, MOVE_WEIGHT_MAX


class TestAddingHomes(TestCase):

    @staticmethod
    def create_home(home_type, listing_provider, price=1500,
                    currently_available=True, num_bedrooms=2,
                    num_bathrooms=2, zip_code="02476", state="MA",
                    last_updated=timezone.now(),
                    date_available=timezone.now()):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=listing_provider,
            last_updated=last_updated,
            date_available=date_available,
        ))

    def test_generate_static_filter_home_list_hunter(self):
        """
        Tests that if the user is a hunter, then it doesn't matter
        what the provider is, they receive all listings
        :return:
        """
        # Arrange
        user = MyUser.objects.create(email="test@email.com", is_hunter=True)
        home_type = HomeTypeModel.objects.create(home_type='House')
        mls_provider = HomeProviderModel.objects.create(provider="MLSPIN")
        ygl_provider = HomeProviderModel.objects.create(provider="YGL")
        survey = RentingSurveyModel.create_survey(user.userProfile, num_bedrooms=[2], max_price=3000)
        survey.home_type.add(home_type)

        # Create homes
        self.create_home(home_type, mls_provider, price=2000)
        self.create_home(home_type, ygl_provider, price=2500)
        self.create_home(home_type, mls_provider, price=3000)

        # Act
        base_algorithm = CocoonAlgorithm()

        # Assert
        self.assertEqual(base_algorithm.generate_static_filter_home_list(survey).count(), 3)

    def test_outdated_homes_eliminated(self):
        """
        Tests that homes with outdated last_updated fields (i.e. last_updated doesn't match last_updated_feed
        in its home provider) are eliminated in the static filter
        :return:
        """
        # Arrange
        user = MyUser.objects.create(email="test@email.com", is_hunter=True)
        home_type = HomeTypeModel.objects.create(home_type='House')
        mls_provider = HomeProviderModel.objects.create(provider="MLSPIN")
        ygl_provider = HomeProviderModel.objects.create(provider="YGL")
        survey = RentingSurveyModel.create_survey(user.userProfile, num_bedrooms=[2], max_price=3000)
        survey.home_type.add(home_type)

        current_time = timezone.now()
        mls_provider.last_updated_feed = current_time
        ygl_provider.last_updated_feed = current_time

        # Create homes
        offmarket_home = self.create_home(home_type, mls_provider, price=2000, last_updated=current_time - timezone.timedelta(days=1))
        onmarket_home = self.create_home(home_type, ygl_provider, price=2500, last_updated=current_time)

        # Act
        base_algorithm = CocoonAlgorithm()

        # Assert
        qs = base_algorithm.generate_static_filter_home_list(survey)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.filter(id=offmarket_home.home.id).exists(), False)
        self.assertEqual(qs.filter(id=onmarket_home.home.id).exists(), True)

    def test_move_in_range_valid(self):
        """
        Tests that if there are three homes in the move in range, then
            the static query gets them
        """
        # Arrange
        user = MyUser.objects.create(email="test@email.com", is_hunter=True)
        home_type = HomeTypeModel.objects.create(home_type='House')
        mls_provider = HomeProviderModel.objects.create(provider="MLSPIN")
        ygl_provider = HomeProviderModel.objects.create(provider="YGL")

        move_in_start_date = timezone.now()
        move_in_end_date = timezone.now() + timedelta(days=12)
        date_available = timezone.now() + timedelta(days=10)
        date_available1 = timezone.now() + timedelta(days=8)
        date_available2 = timezone.now() + timedelta(days=5)

        survey = RentingSurveyModel.create_survey(user.userProfile, num_bedrooms=[2], max_price=3000,
                                    earliest_move_in=move_in_start_date, latest_move_in=move_in_end_date)
        survey.home_type.add(home_type)

        # Create homes
        home = self.create_home(home_type, mls_provider, price=2000, date_available=date_available)
        home1 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available1)
        home2 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available2)

        # Act
        base_algorithm = CocoonAlgorithm()
        qs = base_algorithm.generate_static_filter_home_list(survey)

        # Assert
        self.assertEqual(qs.count(), 3)

    def test_move_in_range_one_home_not_in_range(self):
        """
        Tests that if the move in range for a home is either greater than the move_in_end date or before the move_in
            start date then the homes don't show up
        """
        # Arrange
        user = MyUser.objects.create(email="test@email.com", is_hunter=True)
        home_type = HomeTypeModel.objects.create(home_type='House')
        mls_provider = HomeProviderModel.objects.create(provider="MLSPIN")
        ygl_provider = HomeProviderModel.objects.create(provider="YGL")

        move_in_start = timezone.now()
        move_in_end = timezone.now() + timedelta(days=9 - DAYS_AFTER_MOVE_IN_ADDED)
        date_available = timezone.now() + timedelta(days=10)
        date_available1 = timezone.now() + timedelta(days=8)
        date_available2 = timezone.now() - timedelta(days=1 + DAYS_BEFORE_MOVE_IN_ADDED)

        survey = RentingSurveyModel.create_survey(user.userProfile, num_bedrooms=[2], max_price=3000,
                                    earliest_move_in=move_in_start, latest_move_in=move_in_end,
                                    move_weight=MOVE_WEIGHT_MAX-1)
        survey.home_type.add(home_type)

        # Create homes
        home = self.create_home(home_type, mls_provider, price=2000, date_available=date_available)
        home1 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available1)
        home2 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available2)

        # Act
        base_algorithm = CocoonAlgorithm()
        qs = base_algorithm.generate_static_filter_home_list(survey)

        # Assert
        self.assertEqual(qs.count(), 1)
        self.assertFalse(qs.filter(id=home.home.id).exists())
        self.assertTrue(qs.filter(id=home1.home.id).exists())
        self.assertFalse(qs.filter(id=home2.home.id).exists())

    def test_move_in_range_one_home_in_range_border(self):
        """
        Tests that if the home is on the border, aka on the same day as the move_in start and end period,
            then the home is included
        """
        # Arrange
        user = MyUser.objects.create(email="test@email.com", is_hunter=True)
        home_type = HomeTypeModel.objects.create(home_type='House')
        mls_provider = HomeProviderModel.objects.create(provider="MLSPIN")
        ygl_provider = HomeProviderModel.objects.create(provider="YGL")

        move_in_start = timezone.now()
        move_in_end = timezone.now() + timedelta(days=10 - DAYS_AFTER_MOVE_IN_ADDED)
        date_available = timezone.now() + timedelta(days=10)
        date_available1 = timezone.now() + timedelta(days=8)
        date_available2 = timezone.now() - timedelta(days=DAYS_BEFORE_MOVE_IN_ADDED)

        survey = RentingSurveyModel.create_survey(user.userProfile, num_bedrooms=[2], max_price=3000,
                                    earliest_move_in=move_in_start, latest_move_in=move_in_end,
                                    move_weight=MOVE_WEIGHT_MAX-1)
        survey.home_type.add(home_type)

        # Create homes
        home = self.create_home(home_type, mls_provider, price=2000, date_available=date_available)
        home1 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available1)
        home2 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available2)

        # Act
        base_algorithm = CocoonAlgorithm()
        qs = base_algorithm.generate_static_filter_home_list(survey)

        # Assert
        self.assertEqual(qs.count(), 3)
        self.assertTrue(qs.filter(id=home.home.id).exists())
        self.assertTrue(qs.filter(id=home1.home.id).exists())
        self.assertTrue(qs.filter(id=home2.home.id).exists())

    def test_that_if_the_move_weight_is_max_then_use_currently_available(self):
        """
        Tests that if the move_weight is max, then the date available is ignored
        """
        # Arrange
        user = MyUser.objects.create(email="test@email.com", is_hunter=True)
        home_type = HomeTypeModel.objects.create(home_type='House')
        mls_provider = HomeProviderModel.objects.create(provider="MLSPIN")
        ygl_provider = HomeProviderModel.objects.create(provider="YGL")

        move_in_start = timezone.now()
        move_in_end = timezone.now() + timedelta(days=9 - DAYS_AFTER_MOVE_IN_ADDED)
        date_available = timezone.now() + timedelta(days=10)
        date_available1 = timezone.now() + timedelta(days=8)
        date_available2 = timezone.now() - timedelta(days=1 + DAYS_BEFORE_MOVE_IN_ADDED)

        survey = RentingSurveyModel.create_survey(user.userProfile, num_bedrooms=[2], max_price=3000,
                                    earliest_move_in=move_in_start, latest_move_in=move_in_end,
                                    move_weight=MOVE_WEIGHT_MAX)
        survey.home_type.add(home_type)

        # Create homes
        home = self.create_home(home_type, mls_provider, price=2000, date_available=date_available,
                                currently_available=True)
        home1 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available1,
                                 currently_available=False)
        home2 = self.create_home(home_type, ygl_provider, price=2500, date_available=date_available2,
                                 currently_available=True)

        # Act
        base_algorithm = CocoonAlgorithm()
        qs = base_algorithm.generate_static_filter_home_list(survey)

        # Assert
        self.assertEqual(qs.count(), 2)
        self.assertTrue(qs.filter(id=home.home.id).exists())
        self.assertFalse(qs.filter(id=home1.home.id).exists())
        self.assertTrue(qs.filter(id=home2.home.id).exists())

