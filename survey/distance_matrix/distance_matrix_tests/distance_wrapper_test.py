import unittest
from survey.distance_matrix import distance_wrapper

class TestDistanceWrapper(unittest.TestCase):

    def test_one_destination(self):
        wrapper = distance_wrapper.DistanceWrapper()
        destination = ["2 Snow Hill Lane, Medfield MA"]
        origins = ["1 Dewing Path, Wellesley MA"]
        durations = wrapper.calculate_distances(destination, origins)
        print(durations)
