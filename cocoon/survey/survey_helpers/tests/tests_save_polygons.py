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
            the polygons are saved to the survey. This tests one polygon was passed in
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

    def test_valid_polygons_2_draw_on_map(self):
        """
        Tests that if the user choose to draw polygons on map and polygons were passed in the,
            the polygons are saved to the survey. This tests two polygons were passed in.
        """
        # Arrange
        filter_type = 1
        user = MyUser.objects.create(email="test@email.com")
        survey = RentingSurveyModel.objects.create(user_profile=user.userProfile)
        polygons = [
            {'key': 1, 'vertices': [{'lat': 42.400677237104745, 'lng': -71.12722122802734},
                                    {'lat': 42.36415890370297, 'lng': -70.9768458618164},
                                    {'lat': 42.31035715086906, 'lng': -71.11074173583984}]},
            {'key': 2, 'vertices': [{'lat': 43.400677237104745, 'lng': -69.12722122802734},
                                    {'lat': 41.36415890370297, 'lng': -72.9768458618164},
                                    {'lat': 39.31035715086906, 'lng': -70.11074173583984}]},
        ]

        # Act
        save_polygons(survey, polygons, filter_type)

        # Assert
        self.assertEqual(PolygonModel.objects.count(), 2)
        self.assertEqual(VertexModel.objects.count(), 6)

        # Assert the vertices were created
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('42.400677'), lng=Decimal('-71.127221')).exists())
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('42.364159'), lng=Decimal('-70.976846')).exists())
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('42.310357'), lng=Decimal('-71.110742')).exists())

        self.assertTrue(VertexModel.objects.filter(lat=Decimal('43.400677'), lng=Decimal('-69.127221')).exists())
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('41.364159'), lng=Decimal('-72.976846')).exists())
        self.assertTrue(VertexModel.objects.filter(lat=Decimal('39.310357'), lng=Decimal('-70.110742')).exists())

    def test_two_vertex_polygons_draw_on_map(self):
        """
        Tests that if a polygon with only two vertices are passed in, then the polygon is not saved
        """
        # Arrange
        filter_type = 1
        user = MyUser.objects.create(email="test@email.com")
        survey = RentingSurveyModel.objects.create(user_profile=user.userProfile)
        polygons = [{'key': 1, 'vertices': [{'lat': 42.400677237104745, 'lng': -71.12722122802734},
                                            {'lat': 42.31035715086906, 'lng': -71.11074173583984}]}]

        # Act
        save_polygons(survey, polygons, filter_type)

        # Assert
        self.assertEqual(PolygonModel.objects.count(), 0)
        self.assertEqual(VertexModel.objects.count(), 0)

    def test_one_vertex_polygons_draw_on_map(self):
        """
        Tests that if a polygon with only one vertex is passed in then it is not saved
        """
        # Arrange
        filter_type = 1
        user = MyUser.objects.create(email="test@email.com")
        survey = RentingSurveyModel.objects.create(user_profile=user.userProfile)
        polygons = [{'key': 1, 'vertices': [{'lat': 42.400677237104745, 'lng': -71.12722122802734}]}]

        # Act
        save_polygons(survey, polygons, filter_type)

        # Assert
        self.assertEqual(PolygonModel.objects.count(), 0)
        self.assertEqual(VertexModel.objects.count(), 0)

    def test_delete_old_polygons_before_adding_new_ones(self):
        """
        Tests that if there are any polygons already saved to the account,
        :return:
        """
        # Arrange
        filter_type = 1
        user = MyUser.objects.create(email="test@email.com")
        survey = RentingSurveyModel.objects.create(user_profile=user.userProfile)

        # Creates a polygon already saved
        polygon = survey.polygons.create()
        polygon.vertices.create(lat=45.454545, lng=12.23232)
        # Creates the new polygon being passed in
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
        self.assertFalse(VertexModel.objects.filter(lat=Decimal('45.454545'), lng=Decimal('12.23232')).exists())
