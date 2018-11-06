from django.test import TestCase
from cocoon.scheduler.clientScheduler.client_scheduler import clientSchedulerAlgorithm


class TestClientSchedulerAlgorithm(TestCase):

    def setUp(self):
        self.algorithm = clientSchedulerAlgorithm()

    def test_equal_distance(self):
        '''
        Algorithm Walk Through:

        Step 1: Looks for global minimum starting with row 0: finds it at row 1. So route is 0 -> 1
        Step 2: From 1, look for next minimum that is not 0,1, which is 2. So route is 0 -> 1 -> 2
        Step 3: From 2, look for next minimum that is not 0,1,2, which is 3. So route is 0 -> 1 -> 2 -> 3
        Step 4: From 3, look for the next minimum that is not 0,1,2,3, which is 4. So route is 0 -> 1 -> 2 -> 3 -> 4
        Step 5: All the nodes have been visited, so this is our shortest route

        :return: True
        '''

        distance_matrix_equal = [[0, 1, 1, 1, 1],
                                 [1, 0, 1, 1, 1],
                                 [1, 1, 0, 1, 1],
                                 [1, 1, 1, 0, 1],
                                 [1, 1, 1, 1, 0]]

        equal_path = self.algorithm.calculate_path(distance_matrix_equal)
        self.assertEqual(equal_path, [0, 1, 2, 3, 4])

    def test_increasing_distance(self):
        '''
        Algorithm Walk Through:

        Step 1: Looks for global minimum starting with row 0: finds it at row 1 (distance 2). So route is 0 -> 1
        Step 2: From 1, look for next minimum that is not 0,1, which is 2 (distance 8). So route is 0 -> 1 -> 2
        Step 3: From 2, look for next minimum that is not 0,1,2, which is 3 (distance 14). So route is 0 -> 1 -> 2 -> 3
        Step 4: From 3, look for the next minimum that is not 0,1,2,3, which is 4 (distance 20). So route is 0 -> 1 -> 2 -> 3 -> 4
        Step 5: All the nodes have been visited, so this is our shortest route

        :return: True
        '''

        distance_matrix_increasing = [[0, 2, 3, 4, 5],
                                      [2, 0, 8, 9, 10],
                                      [3, 8, 0, 14, 15],
                                      [4, 9, 14, 0, 20],
                                      [5, 10, 15, 20, 0]]

        increasing_path = self.algorithm.calculate_path(distance_matrix_increasing)
        self.assertEqual(increasing_path, [0, 1, 2, 3, 4])

    def test_decreasing_distance(self):
        '''
        Algorithm Walk Through:

        Step 1: Looks for global minimum starting with row 0: finds it at row 3 (minimum distance of 5). So route is 3 -> 4
        Step 2: From 4, look for next minimum that is not 3,4, which is 2 (dist 11). So route is 3 -> 4 -> 2
        Step 3: From 2, look for next minimum that is not 3,4,2, which is 1 (dist 14). So route is 3 -> 4 -> 2 -> 1
        Step 4: From 1, look for the next minimum that is not 3,4,2,1, which is 0 (dist 20). So route is 3 -> 4 -> 2 -> 1 -> 0
        Step 5: All the nodes have been visited, so this is our shortest route

        :return: True
        '''
        distance_matrix_decreasing = [[0, 20, 15, 10, 21],
                                      [20, 0, 14, 17, 16],
                                      [15, 14, 0, 12, 11],
                                      [10, 17, 12, 0, 5],
                                      [21, 16, 11, 5, 0]]

        decreasing_path = self.algorithm.calculate_path(distance_matrix_decreasing)
        self.assertEqual(decreasing_path, [3, 4, 2, 1, 0])

    def test_3x3_matrix(self):
        '''
        Algorithm Walk Through:

        Step 1: Looks for global minimum starting with row 0: finds it at row 0 (minimum distance of 1). So route is 0 -> 1
        Step 2: From 1, look for next minimum that is not 0,1, which is 2 (dist 1). So route is 0 -> 1 -> 2
        Step 3: All the nodes have been visited, so this is our shortest route

        :return: True
        '''

        distance_matrix_3x3 = [[0, 1, 1],
                               [1, 0, 1],
                               [1, 1, 0]]

        small_matrix_path = self.algorithm.calculate_path(distance_matrix_3x3)
        self.assertEqual(small_matrix_path, [0,1,2])

    def test_closer_father_homes(self):
        '''
        Algorithm Walk Through:

        Step 1: Looks for global minimum starting with row 0: finds it at row 0 (minimum distance of 1). So route is 0 -> 1
        Step 2: From 1, look for next minimum that is not 0,1, which is 2 (dist 1). So route is 0 -> 1 -> 2
        Step 3: All the nodes have been visited, so this is our shortest route

        :return: True
        '''
        distance_matrix_closer_farther = [[0, 1, 10],
                                          [1, 0, 15],
                                          [10, 15, 0]]

        closer_farther_path = self.algorithm.calculate_path(distance_matrix_closer_farther)
        self.assertEqual(closer_farther_path, [0,1,2])

    def test_closer_farther_opposite(self):
        '''
        Algorithm Walk Through:

        Step 1: Looks for global minimum starting with row 0: finds it at row 0 (minimum distance of 1). So route is 0 -> 2
        Step 2: From 2, look for next minimum that is not 0,2, which is 1 (dist 1). So route is 0 -> 2 -> 1
        Step 3: All the nodes have been visited, so this is our shortest route

        :return: True
        '''

        distance_matrix_opposite = [[0, 15, 1],
                                    [15, 0, 1],
                                    [1, 1, 0]]

        opposite_path = self.algorithm.calculate_path(distance_matrix_opposite)
        self.assertEqual(opposite_path, [0,2,1])

