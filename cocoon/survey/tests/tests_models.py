# Import Django Modules
from django.test import TestCase

# Import Survey Models and forms
from cocoon.survey.models import RentingSurveyModel
from cocoon.userAuth.models import MyUser


class TestRentSurveyModelMultipleNames(TestCase):

    def setUp(self):
        # Create user for survey
        self.user = MyUser.objects.create(email="test@email.com")

    @staticmethod
    def create_survey(user_profile, max_price=1500, desired_price=0, max_bathroom=2, min_bathroom=0,
                      num_bedrooms=2, name="Recent Rent Survey"):
        return RentingSurveyModel.objects.create(
            name=name,
            user_profile=user_profile,
            max_price=max_price,
            desired_price=desired_price,
            max_bathrooms=max_bathroom,
            min_bathrooms=min_bathroom,
            num_bedrooms=num_bedrooms,
        )

    def testAddingHomeWithOutOneExisting(self):
        """
        This test that if you add a home and there are no other surveys. The survey is
            sucessfully created and exists in the database
        """
        # Arrange
        survey = self.create_survey(self.user.userProfile)

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 1)
        self.assertEqual(RentingSurveyModel.objects.first(), survey)

    def testAddingHomeWithOneExistingDifferentNames(self):
        """
        This test2 that if you add two surveys with different names then both will be added
            and exist
        """
        # Arrange
        # Create the first survey
        survey1 = self.create_survey(self.user.userProfile, name="Recent Rent Survey")

        survey2 = self.create_survey(self.user.userProfile, name="Test 2")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 2)
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey1.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey2.name))

    def testAddingHomeWithOneExistingSameName(self):
        """
        This test2 that if you add two surveys with the same name, the first survey will
            be overwritten and deleted before saving the second survey
        """
        # Arrange
        # Create the first survey
        self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        survey2 = self.create_survey(self.user.userProfile, name="Recent Rent Survey")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 1)
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey2.name))

    def testAddingHomeWithTwoExistingSameNamePlusOthers(self):
        """
        This test2 that if you add mutiple with the same name, only the last one will persist.
            Also checks to make sure other surveys are not effected
        """
        # Arrange
        # Create the first survey
        self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        survey1 = self.create_survey(self.user.userProfile, name="Some Random Name")
        self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        survey2 = self.create_survey(self.user.userProfile, name="Recent Rent Survey")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 2)
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey2.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey1.name))

    def testAddingHomeWithOneExistingSameNameDifferentUsers(self):
        """
        Test that surveys from other users are not effected. If two surveys from different users
            have the same name, then it should not touch them, aka delete them
        """
        # Arrange
        user2 = MyUser.objects.create(email="test2@test.com")

        # Create the first survey
        survey = self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        survey2 = self.create_survey(user2.userProfile, name="Recent Rent Survey")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 2)
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey2.name))

    def testAddingHomeWithOneExistingSameNameMultipleUsers(self):
        """
        Tests that even with 3 users, the condition still holds
        """
        # Arrange
        user2 = MyUser.objects.create(email="test2@test.com")
        user3 = MyUser.objects.create(email="test3@test.com")

        # Create the first survey
        survey = self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        survey2 = self.create_survey(user2.userProfile, name="Recent Rent Survey")
        survey3 = self.create_survey(user3.userProfile, name="Recent Rent Survey")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 3)
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey2.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey3.name))

    def testAddingHomeWithOneExistingSameNameMultipleUsersAllHaveMultiple(self):
        """
        Tests a complex scenario where two users have duplicates and one doesn't. Makes sure
            the functionality works
        """
        # Arrange
        user2 = MyUser.objects.create(email="test2@test.com")
        user3 = MyUser.objects.create(email="test3@test.com")

        # Create the first survey
        survey = self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        survey2 = self.create_survey(user2.userProfile, name="Recent Rent Survey")
        survey3 = self.create_survey(user3.userProfile, name="Recent Rent Survey")
        self.create_survey(self.user.userProfile, name="Recent Rent Survey")
        self.create_survey(user2.userProfile, name="Recent Rent Survey")
        survey4 = self.create_survey(user3.userProfile, name="Test Survey")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 4)
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey2.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey3.name))
        self.assertTrue(RentingSurveyModel.objects.filter(name=survey4.name))

    def testAddingHomeWithSameSlugDifferentName(self):
        """
        Tests that is the name are different but the slug names are the same. Then only one
            will exist
        """
        # Arrange
        # Create the first survey
        survey1 = self.create_survey(self.user.userProfile, name="Recents")

        survey2 = self.create_survey(self.user.userProfile, name="Recent's")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 1)
        self.assertTrue(RentingSurveyModel.objects.filter(url=survey2.url))

    def testAddingHomeWithSameSlugDifferentNameDifferentUsers(self):
        """
        Tests that is the names are different but the slugs names are the same but they
            are from different users, then they both will exist
        """
        # Arrange
        user2 = MyUser.objects.create(email="test2@test.com")
        # Create the first survey
        survey1 = self.create_survey(self.user.userProfile, name="Recents")

        survey2 = self.create_survey(user2.userProfile, name="Recent's")

        # Assert
        self.assertEqual(RentingSurveyModel.objects.count(), 2)
        self.assertTrue(RentingSurveyModel.objects.filter(url=survey1.url))
        self.assertTrue(RentingSurveyModel.objects.filter(url=survey2.url))
