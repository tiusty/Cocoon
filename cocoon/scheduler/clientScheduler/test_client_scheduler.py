from django.test import TestCase
from .client_scheduler import clientSchedulerAlgorithm


class TestClientSchedulerAlgorithm(TestCase):

    def setUp(self):
        self.algorithm = clientSchedulerAlgorithm()

    def test_equal_distance(self):
        distance_matrix_equal = [[0, 1, 1, 1, 1],
                                 [1, 0, 1, 1, 1],
                                 [1, 1, 0, 1, 1],
                                 [1, 1, 1, 0, 1],
                                 [1, 1, 1, 1, 0]]

        equal_path = self.algorithm.calculate_path(distance_matrix_equal)
        self.assertEqual(equal_path, [0, 1, 2, 3, 4])

    def test_increasing_distance(self):
        distance_matrix_increasing = [[0, 2, 3, 4, 5],
                                      [2, 0, 8, 9, 10],
                                      [3, 8, 0, 14, 15],
                                      [4, 9, 14, 0, 20],
                                      [5, 10, 15, 20, 0]]

        increasing_path = self.algorithm.calculate_path(distance_matrix_increasing)
        self.assertEqual(increasing_path, [0, 1, 2, 3, 4])

    def test_decreasing_distance(self):
        distance_matrix_decreasing = [[0, 20, 15, 10, 21],
                                      [20, 0, 14, 17, 16],
                                      [15, 14, 0, 12, 11],
                                      [10, 17, 12, 0, 5],
                                      [21, 16, 11, 5, 0]]

        decreasing_path = self.algorithm.calculate_path(distance_matrix_decreasing)
        self.assertEqual(decreasing_path, [3, 4, 2, 1, 0])

    def test_3x3_matrix(self):
        distance_matrix_3x3 = [[0, 1, 1],
                               [1, 0, 1],
                               [1, 1, 0]]

        small_matrix_path = self.algorithm.calculate_path(distance_matrix_3x3)
        print(small_matrix_path)

    def test_closer_father_homes(self):
        distance_matrix_closer_farther = [[0, 1, 10],
                                          [1, 0, 15],
                                          [10, 15, 0]]

        closer_farther_path = self.algorithm.calculate_path(distance_matrix_closer_farther)
        print(closer_farther_path)

    def test_closer_farther_opposite(self):
        distance_matrix_opposite = [[0, 15, 1],
                                    [15, 0, 1],
                                    [1, 1, 0]]

        opposite_path = self.algorithm.calculate_path(distance_matrix_opposite)
        print(opposite_path)

