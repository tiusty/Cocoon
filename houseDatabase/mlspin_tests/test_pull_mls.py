from django.test import TestCase
from houseDatabase.models import RentDatabaseModel, HomeTypeModel
import os

# Import script to pull MLSPIN data
from houseDatabase.management.commands.pull_mlspin import MlspinRequester

class TestPullMlspin(TestCase):

    """"
    reads in a file with test data and passes it to the Mls requester
    """
    def setUp(self):

        # Set up the apartment home type

        HomeTypeModel.objects.create(home_type_survey="Apartment")
        idx_file = open(os.path.join(os.path.dirname(__file__), "test_idx_feed.txt"), "rb")
        self.idx_data = (idx_file.read().decode("iso-8859-1"))

        towns_file = open(os.path.join(os.path.dirname(__file__), "test_towns.txt"), "rb")
        self.towns_data = (towns_file.read().decode("iso-8859-1"))

        self.mls_handler = MlspinRequester(self.idx_data, self.towns_data)

    def test_idx_parser(self):

        self.mls_handler.parse_idx_feed()

        # assert that the homes exist in the database
        self.assertEqual(len(RentDatabaseModel.objects.all()), 3)

        home1 = RentDatabaseModel.objects.get(pk=1) # 12 Mount Vernon St.
        home2 = RentDatabaseModel.objects.get(pk=2) # 296 Marlborough St.
        home3 = RentDatabaseModel.objects.get(pk=3) # 784 Tremont St.

        self.assertEqual(home1.street_address_home, "12 Mount Vernon St.")
        self.assertEqual(home1.city_home, "Boston")
        self.assertEqual(home1.zip_code_home, "02129")
        self.assertEqual(home1.price_home, 3800)
