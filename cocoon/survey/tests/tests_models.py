# Import Django Modules
from django.test import TestCase

# Import Survey Models and forms
from cocoon.survey.models import RentingSurveyModel, HomeInformationModel
from cocoon.userAuth.models import MyUser


class TestHomeInformationModel(TestCase):

    def test_num_bedrooms_getter(self):
        # Arrange
        survey = HomeInformationModel()

        # i.e they choose only studio
        num_bedrooms_mask = 1
        # Only 1 bedroom
        num_bedrooms_mask1 = 2
        # Only 2 bedrooms
        num_bedrooms_mask2 = 4
        # Only 3 bedrooms
        num_bedrooms_mask3 = 8
        # Only 4 bedrooms
        num_bedrooms_mask4 = 16
        # 1 + 3 bedrooms
        num_bedrooms_mask13 = 10
        # 0 + 2 bedrooms
        num_bedrooms_mask02 = 5
        # 1 + 3 + 4 bedrooms
        num_bedrooms_mask134 = 26
        # 0 + 1 + 2 + 3 + 4 bedrooms
        num_bedrooms_mask01234 = 31

        # Act
        survey.num_bedrooms_bit_masked = num_bedrooms_mask
        self.assertEqual([0], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask1
        self.assertEqual([1], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask2
        self.assertEqual([2], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask3
        self.assertEqual([3], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask4
        self.assertEqual([4], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask13
        self.assertEqual([1, 3], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask02
        self.assertEqual([0, 2], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask134
        self.assertEqual([1, 3, 4], survey.num_bedrooms)
        survey.num_bedrooms_bit_masked = num_bedrooms_mask01234
        self.assertEqual([0, 1, 2, 3, 4], survey.num_bedrooms)

    def test_num_bedrooms_setter(self):
        # Arrange
        survey = HomeInformationModel()




