from django.test import TestCase
from django.utils import timezone

# Cocoon modules
from cocoon.survey.models import RentingSurveyModel
from cocoon.userAuth.models import MyUser
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel, HomeProviderModel
from cocoon.survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm
from cocoon.survey.home_data.home_score import HomeScore


class TestAddingHomes(TestCase):

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
    def create_home(home_type, listing_provider, price=1500,
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA",last_updated=timezone.now()):
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
        survey = self.create_survey(user.userProfile, num_bedrooms=2, max_price=3000)
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
        survey = self.create_survey(user.userProfile, num_bedrooms=2, max_price=3000)
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

