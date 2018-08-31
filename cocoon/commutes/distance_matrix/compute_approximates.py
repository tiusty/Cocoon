# import houseDatabase models
from cocoon.commutes.models import ZipCodeBase

# import distance matrix wrapper
from cocoon.commutes.distance_matrix.distance_wrapper import DistanceWrapper


def approximate_commute_handler(origins_zips_states, destination_zip_state, commute_type_query):
    """
    approximate_commute_handler stands between the rent_algorithm and the distance_wrapper,
    calling the distance matrix on the provided origins and destination and updates the
    ZipCodeParent and ZipCodeChildModel models accordingly.

    :param: origin_zips_states, list(tuple(string, string)) a list of tuples strings
    with zip code and state
    :param: destination_zip_state, tuple(string, string), a tuple of zip code and state as strings
    :param: commute_type (CommuteType): The commute the user desires

    Example Input:
        origins = [("02123", "MA"), ("02012", Maine), ("12345", NY)]
        destination = ("20344", California)
        commute_type = "driving"
    """

    wrapper = DistanceWrapper()

    # map (zip, state) tuples list to a list of "state+zip" strings
    results = wrapper.get_durations_and_distances(list(map(lambda x:x[1]+"+"+x[0], origins_zips_states)),
                                                  [destination_zip_state[1]+"+"+destination_zip_state[0]],
                                                  mode=commute_type_query.commute_type)

    # iterates both lists simultaneously
    for origin, result in zip(origins_zips_states, results):
        if ZipCodeBase.objects.filter(zip_code=origin[0]).exists():
            zip_code_dictionary = ZipCodeBase.objects.get(zip_code=origin[0])
            zip_dest = zip_code_dictionary.zipcodechild_set.filter(
                    zip_code=destination_zip_state[0],
                    commute_type=commute_type_query)

            # If the zip code doesn't exist or is not valid then compute the approximate distance
            #   If the zip code was not valid then delete it first before recomputing it
            if not zip_dest.exists() or not zip_dest.first().zip_code_cache_still_valid():
                if zip_dest.exists():
                    zip_dest.delete()
                zip_code_dictionary.zipcodechild_set.create(
                    zip_code=destination_zip_state[0],
                    commute_type=commute_type_query,
                    commute_distance_meters=result[0][1],
                    commute_time_seconds=result[0][0],
                )
        else:
            ZipCodeBase.objects.create(zip_code=origin[0]) \
                .zipcodechild_set.create(
                zip_code=destination_zip_state[0],
                commute_type=commute_type_query,
                commute_distance_meters=result[0][1],
                commute_time_seconds=result[0][0],
            )