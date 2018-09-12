# Django modules
from django.test import TestCase
from django.utils import timezone

# Cocoon modules
from cocoon.houseDatabase.management.commands.ygl.YGLRequester import YGLRequester
from cocoon.houseDatabase.models import YglManagementModel, HomeTypeModel, RentDatabaseModel, HomeProviderModel


class TestYGLRequester(TestCase):

    def setUp(self):

        # Create the manager
        YglManagementModel.objects.create()
        HomeProviderModel.objects.create(provider="YGL")

        # Set up the apartment home type
        self.home_type = HomeTypeModel.objects.create(home_type="Apartment")

    def test_pulling_homes(self):
        """
        Make sure that the ygl puller can pull in homes correctly
        """
        # Arrange
        ygl_requester = YGLRequester(timezone.now(), ygl_file='ygl_tests/test_ygl_feed.xml')

        # Act
        ygl_requester.parse_idx_feed()

        # Retrieve homes
        home1 = RentDatabaseModel.objects.get(street_address_home="7 Lothian Rd")
        home2 = RentDatabaseModel.objects.get(street_address_home="16 Wadsworth St")
        home3 = RentDatabaseModel.objects.get(street_address_home="31 Claymoss Rd")

        # Assert

        # Assert first home
        self.assertEqual(home1.street_address, "7 Lothian Rd")
        self.assertEqual(home1.city, "Boston")
        self.assertEqual(home1.zip_code, "02135")
        self.assertEqual(home1.price, 2000)
        self.assertEqual(home1.home_type, self.home_type)
        self.assertEqual(str(home1.latitude), str(42.340347))
        self.assertEqual(str(home1.longitude), str(-71.153633))
        self.assertEqual(home1.state, "MA")
        self.assertEqual(home1.num_bedrooms, 2)
        self.assertEqual(home1.num_bathrooms, 1)
        self.assertEqual(home1.listing_number, 121307521)
        self.assertEqual(home1.listing_provider, HomeProviderModel.objects.get(provider="YGL"))
        self.assertEqual(home1.listing_office, '')

        # Assert second home
        self.assertEqual(home2.street_address, "16 Wadsworth St")
        self.assertEqual(home2.city, "Boston")
        self.assertEqual(home2.zip_code, "02134")
        self.assertEqual(home2.price, 5000)
        self.assertEqual(home2.home_type, self.home_type)
        self.assertEqual(str(home2.latitude), str(42.355179))
        self.assertEqual(str(home2.longitude), str(-71.125954))
        self.assertEqual(home2.state, "MA")
        self.assertEqual(home2.num_bedrooms, 4)
        self.assertEqual(home2.num_bathrooms, 2)
        self.assertEqual(home2.listing_number, 121307525)
        self.assertEqual(home2.listing_provider, HomeProviderModel.objects.get(provider="YGL"))
        self.assertEqual(home2.listing_office, '')

        # Assert third home
        self.assertEqual(home3.street_address, "31 Claymoss Rd")
        self.assertEqual(home3.city, "Boston")
        self.assertEqual(home3.zip_code, "02135")
        self.assertEqual(home3.price, 2700)
        self.assertEqual(home3.home_type, self.home_type)
        self.assertEqual(str(home3.latitude), '42.344400')
        self.assertEqual(str(home3.longitude), '-71.145100')
        self.assertEqual(home3.state, "MA")
        self.assertEqual(home3.num_bedrooms, 3)
        self.assertEqual(home3.num_bathrooms, 1)
        self.assertEqual(home3.listing_number, 121307530)
        self.assertEqual(home3.listing_provider, HomeProviderModel.objects.get(provider="YGL"))
        self.assertEqual(home3.listing_office, '')

