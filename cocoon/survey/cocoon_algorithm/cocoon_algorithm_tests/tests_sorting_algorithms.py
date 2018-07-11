from django.test import TestCase

# Import survey modules
from cocoon.survey.cocoon_algorithm.sorting_algorithms import SortingAlgorithms
from cocoon.survey.home_data.home_score import HomeScore


class TestInsertionSort(TestCase):

    def setUp(self):
        self.home = HomeScore()
        self.home1 = HomeScore()
        self.home2 = HomeScore()
        self.home_list = [self.home, self.home1, self.home2]

    def test_insertion_sort_working(self):
        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = 60
        self.home.total_possible_points = 80
        # Set home 1
        self.home1.accumulated_points = 120
        self.home1.total_possible_points = 150
        # Set home 2
        self.home2.accumulated_points = 340
        self.home2.total_possible_points = 450

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        # Home 0
        self.assertEqual(self.home, self.home_list[2])
        # Home 1
        self.assertEqual(self.home1, self.home_list[0])
        # Home 2
        self.assertEqual(self.home2, self.home_list[1])

    def test_insertion_sort_all_equal_but_different_total_possible_points(self):
        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = 60
        self.home.total_possible_points = 80
        # Set home 1
        self.home1.accumulated_points = 120
        self.home1.total_possible_points = 160
        # Set home 2
        self.home2.accumulated_points = 30
        self.home2.total_possible_points = 40

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        self.assertEqual(self.home, self.home_list[1])
        self.assertEqual(self.home1, self.home_list[0])
        self.assertEqual(self.home2, self.home_list[2])

    def test_insertion_sort_all_equal_but_same_total_possible_points(self):
        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = 60
        self.home.total_possible_points = 80
        # Set home 1
        self.home1.accumulated_points = 60
        self.home1.total_possible_points = 80
        # Set home 2
        self.home2.accumulated_points = 60
        self.home2.total_possible_points = 80

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        self.assertEqual(self.home, self.home_list[0])
        self.assertEqual(self.home1, self.home_list[1])
        self.assertEqual(self.home2, self.home_list[2])

    def test_insertion_sort_some_equal_last(self):
        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = 60
        self.home.total_possible_points = 80
        # Set home 1
        self.home1.accumulated_points = 130
        self.home1.total_possible_points = 160
        # Set home 2
        self.home2.accumulated_points = 120
        self.home2.total_possible_points = 160

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        self.assertEqual(self.home, self.home_list[2])
        self.assertEqual(self.home1, self.home_list[0])
        self.assertEqual(self.home2, self.home_list[1])

    def test_insertion_sort_some_equal_first(self):
        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = 60
        self.home.total_possible_points = 80
        # Set home 1
        self.home1.accumulated_points = 110
        self.home1.total_possible_points = 160
        # Set home 2
        self.home2.accumulated_points = 120
        self.home2.total_possible_points = 160

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        self.assertEqual(self.home, self.home_list[1])
        self.assertEqual(self.home1, self.home_list[2])
        self.assertEqual(self.home2, self.home_list[0])

    def test_insertion_sort_all_zero(self):

        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = 0
        self.home.total_possible_points = 0
        # Set home 1
        self.home1.accumulated_points = 0
        self.home1.total_possible_points = 0
        # Set home 2
        self.home2.accumulated_points = 0
        self.home2.total_possible_points = 0

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        self.assertEqual(self.home, self.home_list[0])
        self.assertEqual(self.home1, self.home_list[1])
        self.assertEqual(self.home2, self.home_list[2])

    def test_insertion_sort_one_negative(self):

        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = 60
        self.home.total_possible_points = 120
        # Set home 1
        self.home1.accumulated_points = -20
        self.home1.total_possible_points = 40
        # Set home 2
        self.home2.accumulated_points = 70
        self.home2.total_possible_points = 120

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        self.assertEqual(self.home, self.home_list[1])
        self.assertEqual(self.home1, self.home_list[2])
        self.assertEqual(self.home2, self.home_list[0])

    def test_insertion_sort_all_negative(self):

        # Arrange
        sorting_algorithm = SortingAlgorithms()
        # Set home 0
        self.home.accumulated_points = -60
        self.home.total_possible_points = 120
        # Set home 1
        self.home1.accumulated_points = -20
        self.home1.total_possible_points = 40
        # Set home 2
        self.home2.accumulated_points = -70
        self.home2.total_possible_points = 120

        # Act
        sorting_algorithm.insertion_sort(self.home_list)

        # Assert
        self.assertEqual(self.home, self.home_list[0])
        self.assertEqual(self.home1, self.home_list[2])
        self.assertEqual(self.home2, self.home_list[1])
