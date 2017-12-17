from django.test import TestCase

from houseDatabase.models import RentDatabase
from survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm


class TestAddingHomes(TestCase):

    def setUp(self):
        self.home = RentDatabase.objects.create()
        self.home1 = RentDatabase.objects.create()

    def test_adding_home(self):
        base_algorithm = CocoonAlgorithm()
        base_algorithm.homes = self.home
        base_algorithm.homes = self.home1
        self.assertEqual(2, len(base_algorithm.homes))