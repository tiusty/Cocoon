from django.test import TestCase
from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel
from cocoon.houseDatabase.models import MlsManagementModel
import os
from datetime import datetime
from decimal import Decimal
# Import script to pull MLSPIN data
from cocoon.houseDatabase.management.commands.pull_mlspin import MlspinRequester


class TestPullMlspin(TestCase):

    """"
    reads in a file with test data and passes it to the Mls requester
    """
    def setUp(self):

        # Set up the apartment home type

        MlsManagementModel.objects.create()

        self.home_type = HomeTypeModel.objects.create(home_type_survey="Apartment")
        idx_file = open(os.path.join(os.path.dirname(__file__), "test_idx_feed.txt"), "rb")
        self.idx_data = (idx_file.read().decode("iso-8859-1"))

        towns_file = open(os.path.join(os.path.dirname(__file__), "test_towns.txt"), "rb")
        self.towns_data = (towns_file.read().decode("iso-8859-1"))

        self.mls_handler = MlspinRequester(self.idx_data, self.towns_data)

    def test_idx_parser(self):

        self.mls_handler.parse_idx_feed()

        # assert that the homes exist in the database
        self.assertEqual(RentDatabaseModel.objects.count(), 3)

        home1 = RentDatabaseModel.objects.get(pk=1) # 12 Mount Vernon St.
        home2 = RentDatabaseModel.objects.get(pk=2) # 296 Marlborough St.
        home3 = RentDatabaseModel.objects.get(pk=3) # 784 Tremont St.

        # asserts for the first home
        self.assertEqual(home1.street_address_home, "12 Mount Vernon St.")
        self.assertEqual(home1.city_home, "Boston")
        self.assertEqual(home1.zip_code_home, "02129")
        self.assertEqual(home1.price_home, 3800)
        self.assertEqual(home1.home_type_home, self.home_type)
        self.assertEqual(str(home1.latitude_home), "42.375699")
        self.assertEqual(str(home1.longitude_home), "-71.058828")
        self.assertEqual(home1.state_home, "MA")
        self.assertEqual(home1.num_bedrooms_home, 2)
        self.assertEqual(home1.num_bathrooms_home, 1)
        self.assertEqual(home1.bath_home, True)
        self.assertEqual(home1.listing_number_home, 71811023)
        self.assertEqual(home1.listing_agent_home, "BB808729")
        self.assertEqual(home1.listing_provider_home, "MLSPIN")
        self.assertEqual(home1.listing_office_home, "AN1037")

        # asserts for the second home
        self.assertEqual(home2.street_address_home, "296 Marlborough St")
        self.assertEqual(home2.city_home, "Boston")
        self.assertEqual(home2.zip_code_home, "02114")
        self.assertEqual(home2.price_home, 2850)
        self.assertEqual(home2.home_type_home, self.home_type)
        self.assertEqual(str(home2.latitude_home), "42.351246")
        self.assertEqual(str(home2.longitude_home), "-71.083828")
        self.assertEqual(home2.state_home, "MA")
        self.assertEqual(home2.num_bedrooms_home, 1)
        self.assertEqual(home2.num_bathrooms_home, 1)
        self.assertEqual(home2.bath_home, True)
        self.assertEqual(home2.listing_number_home, 71738853)
        self.assertEqual(home2.listing_agent_home, "BB808729")
        self.assertEqual(home2.listing_provider_home, "MLSPIN")
        self.assertEqual(home2.listing_office_home, "AN1037")

        # asserts for the third home
        self.assertEqual(home3.street_address_home, "784 Tremont Street")
        self.assertEqual(home3.city_home, "Boston")
        self.assertEqual(home3.zip_code_home, "02118")
        self.assertEqual(home3.price_home, 3460)
        self.assertEqual(home3.home_type_home, self.home_type)
        self.assertEqual(str(home3.latitude_home), "42.338892")
        self.assertEqual(str(home3.longitude_home), "-71.080790")
        self.assertEqual(home3.state_home, "MA")
        self.assertEqual(home3.num_bedrooms_home, 1)
        self.assertEqual(home3.num_bathrooms_home, 1)
        self.assertEqual(home3.bath_home, True)
        self.assertEqual(home3.listing_number_home, 72080819)
        self.assertEqual(home3.listing_agent_home, "BB808729")
        self.assertEqual(home3.listing_provider_home, "MLSPIN")
        self.assertEqual(home3.listing_office_home, "AN1037")