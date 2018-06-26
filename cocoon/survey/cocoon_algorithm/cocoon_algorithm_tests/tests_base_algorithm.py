from django.test import TestCase

from cocoon.houseDatabase.models import RentDatabaseModel, HomeTypeModel
from cocoon.survey.cocoon_algorithm.base_algorithm import CocoonAlgorithm


class TestAddingHomes(TestCase):

    def setUp(self):
        self.home_type = HomeTypeModel.objects.create(home_type_survey='House')
        self.home = RentDatabaseModel.objects.create(home_type_home=self.home_type)
        self.home1 = RentDatabaseModel.objects.create(home_type_home=self.home_type)

    def test_adding_home(self):
        base_algorithm = CocoonAlgorithm()
        base_algorithm.homes = self.home
        base_algorithm.homes = self.home1
        self.assertEqual(2, len(base_algorithm.homes))