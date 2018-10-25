# Retrieve Cocoon Models
from cocoon.commutes.models import CommuteType

# Retrieve Distance Matrix
from cocoon.commutes.distance_matrix.distance_wrapper import DistanceWrapper

# Retrieve Constants
from cocoon.commutes.constants import GoogleCommuteNaming


def retrieve_exact_commute(origins, destinations, mode=CommuteType.DRIVING):
    """
    This wraps the get_durations_and_distances to prevent a user from calling the matrix with the wrong value

    The commute type stored in the database is in a different form then what the google distance matrix accepts.
        Therefore this does the conversion.

    If the mode type is not recognized then an empty list is returned
    :param origins: (list(string)) -> List of values that is accepted by the distance matrix
    :param destinations: (list(destination)) -> list of values that is accepted by the distance matrix
    :param mode: (CommuteType.MODE) -> The commute type that is stored in the commute type format
    :return: (list(tuple)) -> A list of tuples containing the duration and distance between each destination
        and the origin.
    """
    wrapper = DistanceWrapper()
    if mode == CommuteType.DRIVING:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.DRIVING)
    elif mode == CommuteType.TRANSIT:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.TRANSIT)
    elif mode == CommuteType.BICYCLING:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.BICYCLING)
    elif mode == CommuteType.WALKING:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.WALKING)
    else:
        return []
