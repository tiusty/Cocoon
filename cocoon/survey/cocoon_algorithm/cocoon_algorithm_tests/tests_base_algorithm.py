from django.test import TestCase

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
                    currently_available=True, num_bedrooms=2, num_bathrooms=2, zip_code="02476", state="MA"):
        return HomeScore(RentDatabaseModel.objects.create(
            home_type=home_type,
            price=price,
            currently_available=currently_available,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            zip_code=zip_code,
            state=state,
            listing_provider=listing_provider,
        ))

    def test_generate_static_filter_home_list_hunter(self):
        """
        Tests that if the user is a hunter, then it doesn't matter
        what the provider is, they receive all listings
        :return:
        """
        # Arrange
        user = MyUser.objects.create()
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

