# Retrieve Cocoon Models
from cocoon.commutes.models import CommuteType

# Retrieve Distance Matrix
from .distance_wrapper import DistanceWrapper
from ..models import ZipCodeChild, ZipCodeBase
from .home_commute import  HomeCommute

# Retrieve Constants
from cocoon.commutes.constants import GoogleCommuteNaming


def retrieve_exact_commute_client_scheduler(homes, destination, commute_type):
    """
    Exact commute retriever for the client scheduler. Puts the arguments in the correct formation
    :param homes: (list(RentDatabase models)) -> The rent database models used for computation
    :param destination: (RentDatabase Model) -> The destination which other homes compute against
    :param commute_type: (CommuteType) -> The type of commute for the commute
    :return: (list(tuple(time, distance)) -> returns the time as seconds and the distance as meters. Also each index has
        all possible combinations given by google, i.e if there are different routes
    """
    home_addresses = []
    for home in homes:
        home_addresses.append(home.full_address)

    return retrieve_exact_commute(destination.full_address, home_addresses, commute_type)


def retrieve_approximate_commute_client_scheduler(homes, destination, commute_type):
    """
    Approximation commute retriever for the client scheduler. Puts arguments in correct format.
    :param homes: (list(RentDatabase Models)) -> The homes to compute against
    :param destination: (RentDatabase Models) -> The home which all other homes compute against
    :param commute_type: (Commute Type) -> The commute type of the approximation
    :return: (list(ints)) -> Returns the commute time for each home from the destination to that home. It is returned
        in the order it is sent
    """
    return retrieve_approximate_commute(HomeCommute.rentdatabases_to_home_cache(homes),
                                        HomeCommute.rentdatabase_to_home_cache(destination), commute_type)


def retrieve_exact_commute(origins, destinations, mode):
    """
    This wraps the get_durations_and_distances to prevent a user from calling the matrix with the wrong value

    The commute type stored in the database is in a different form then what the google distance matrix accepts.
        Therefore this does the conversion.

    If the mode type is not recognized then an empty list is returned
    :param origins: (list(string)) -> List of values that is accepted by the distance matrix
    :param destinations: (list(destination)) -> list of values that is accepted by the distance matrix
    :param mode: (CommuteType Model) -> The commute type that is stored in the commute type format
    :return: (list(tuple)) -> A list of tuples containing the duration and distance between each destination
        and the origin. If the commute type is not recognized then an empty list is returned
    """
    wrapper = DistanceWrapper()
    if mode.commute_type == CommuteType.DRIVING:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.DRIVING)
    elif mode.commute_type == CommuteType.TRANSIT:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.TRANSIT)
    elif mode.commute_type == CommuteType.BICYCLING:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.BICYCLING)
    elif mode.commute_type == CommuteType.WALKING:
        return wrapper.get_durations_and_distances(origins, destinations, mode=GoogleCommuteNaming.WALKING)
    else:
        return []


def retrieve_approximate_commute(homes, destination, commute_type):
    """
    This wraps the get_durations_and_distances to prevent a user from calling the matrix with the wrong value

    The commute type stored in the database is in a different form then what the google distance matrix accepts.
        Therefore this does the conversion.

    If the mode type is not recognized then an empty list is returned
    :param homes: (list(HomeCommute)) -> List of values that is accepted by the distance matrix
    :param destination: HomeCommute -> list of values that is accepted by the distance matrix
    :param commute_type: (CommuteType Model) -> The commute type that is stored in the commute type format
    :return: (list(tuple)) -> A list of tuples containing the duration and distance between each destination
        and the origin. If the commute type is not recognized then an empty list is returned
    """
    approx = []
    commute_type = CommuteType.objects.get_or_create(commute_type=commute_type)[0]
    try:
        # Retrieve the destination zip_code object if it exists
        destination_zip = ZipCodeBase.objects.get(zip_code=destination.zip_code)

        # Retrieve all the child zip_codes for the destination commute_type
        child_zips = ZipCodeChild.objects.filter(base_zip_code=destination_zip). \
            filter(commute_type=commute_type). \
            values_list('zip_code', 'commute_time_seconds')

        # Dictionary Compression to retrieve the values from the QuerySet
        child_zip_codes = {zip_code: commute_time_seconds for zip_code, commute_time_seconds in child_zips}

        # For every home check to see if a zip code pair exists and then store the commute time
        for home in homes:

            # Determines if the home exists in the dictionary on child_zip_codes
            result = home.zip_code in child_zip_codes

            # If there was a match, (there should only be one)
            if result:
                # Store the commute time associated with the zip_code
                approx.append(child_zip_codes[home.zip_code])
            else:
                approx.append(-1)

    # If the ZipCodeBase doesn't exist then... just don't compute, it should be there if the update_cache function
    # is called before this
    except ZipCodeBase.DoesNotExist:
        for home in homes:
            approx.append(-1)

    return approx
