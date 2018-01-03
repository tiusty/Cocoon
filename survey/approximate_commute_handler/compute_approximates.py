from houseDatabase.models import RentDatabaseModel, HomeTypeModel, ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel
from survey.distance_matrix.distance_wrapper import DistanceWrapper

# TODO: best way to add more specificity than zip code
# TODO: update values after certain length of time
def approximate_compute_handler(origins, destination, commute_type):
    """
    approximate_compute_handler stands between the rent_algorithm and the distance_wrapper,
    calling the distance matrix on the provided origins and destination and updates the
    ZipCodeParent and ZipCodeChildModel models accordingly.

    :param: origins, a list of strings that are 5 digit zip codes
    :param: destination, a string that is the 5 digit zip code destination
    :param: commute_type, a string, either "driving", "transit", "walking", "biking"
    :return: the result of the DistanceWrapper.calculate_distances() call.
        Format is a list of lists of tuples. Each inner list corresponds to an origin
        and each of its tuples contains the duration (in seconds) and distance (in meters)
        from the origin to a destination, in the same order they were given. In this case,
        there will always be 1 destination.

    Example Input:
        origins = ["02123", "02012", "12345"]
        destination = "20344"
        commute_type = "driving"
    Output:
        [[(10349, 394)],[(2343. 423)],[(2342, 3452)]]
    """

    wrapper = DistanceWrapper(mode=commute_type)
    results = wrapper.calculate_distances(origins, [destination])

    # iterates both lists simultaneously
    for origin, result in zip(origins, results):
        if ZipCodeDictionaryParentModel.objects.filter(zip_code_parent=origin).exists():
            zip_code_dictionary = ZipCodeDictionaryParentModel.objects.get(zip_code_parent=origin)
            if zip_code_dictionary.zipcodedictionarychildmodel_set.filter(
                    zip_code_child=destination,
                    commute_type_child=commute_type).exists():
                print("The combination that was computed already exists")
            else:
                zip_code_dictionary.zipcodedictionarychildmodel_set.create(
                    zip_code_child=destination,
                    commute_type_child=commute_type,
                    commute_distance_meters_child=result[1],
                    commute_time_seconds_child=result[0],
                )
                print(result[0])
        else:
            ZipCodeDictionaryParentModel.objects.create(zip_code_parent=origin) \
                .zipcodedictionarychildmodel_set.create(
                zip_code_child=destination,
                commute_type_child=commute_type,
                commute_distance_meters_child=result[1],
                commute_time_seconds_child=result[0],
            )

    return results