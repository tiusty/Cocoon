# Django imports
from django.test import TestCase

# Import file to test
from ..save_polygons import save_polygons

# Import app modules
from ...models import RentingSurveyModel, PolygonModel, VertexModel

# Import cocoon modules
from cocoon.userAuth.models import MyUser

# Import third part modules
from decimal import Decimal


class TestSavePolygons(TestCase):

    def test_valid_polygons_not_on_map(self):
        """
        Tests that even if polygons are returned, if the users choose to not have polygons, then they are not
            saved
        """
        # Arrange
        filter_type = 0
        user = MyUser.objects.create(email="test@email.com")
        survey = RentingSurveyModel.objects.create(user_profile=user.userProfile)
        polygons = [{'key': 1, 'vertices': [{'lat': 42.400677237104745, 'lng': -71.12722122802734},
                                            {'lat': 42.36415890370297, 'lng': -70.9768458618164},
                                            {'lat': 42.31035715086906, 'lng': -71.11074173583984}]}]

        # Act
        save_polygons(survey, polygons, filter_type)

        # Assert
        self.assertEqual(PolygonModel.objects.count(), 0)
        self.assertEqual(VertexModel.objects.count(), 0)

    def test_valid_polygons_draw_on_map(self):
        """
        Tests that if the user choose to draw polygons on map and polygons were passed in the,
            the polygons are saved to the survey
        """
        # Arrange
        filter_type = 1
        user = MyUser.objects.create(email="test@email.com")
        survey = RentingSurveyModel.objects.create(user_profile=user.userProfile)
        polygons = [{'key': 1, 'vertices': [{'lat': 42.400677237104745, 'lng': -71.12722122802734},
                                            {'lat': 42.36415890370297, 'lng': -70.9768458618164},
                                            {'lat': 42.31035715086906, 'lng': -71.11074173583984}]}]

        # Act
        save_polygons(survey, polygons, filter_type)

        # Assert
        self.assertEqual(PolygonModel.objects.count(), 1)
        self.assertEqual(VertexModel.objects.count(), 3)

        # Assert the vertices were created
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('42.400677'), lng=Decimal('-71.127221')).exists())
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('42.364159'), lng=Decimal('-70.976846')).exists())
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('42.310357'), lng=Decimal('-71.110742')).exists())
