from houseDatabase.models import RentDatabaseModel, HomeTypeModel, ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel
from survey.distance_matrix.distance_wrapper import DistanceWrapper

# TODO: best way to add more specificity than zip code
# TODO: update values after certain length of time
def approximate_commute_handler(origins_zips_states, destination_zip_state, commute_type):
    """
    approximate_commute_handler stands between the rent_algorithm and the distance_wrapper,
    calling the distance matrix on the provided origins and destination and updates the
    ZipCodeParent and ZipCodeChildModel models accordingly.

    :param: origin_zips_states, list(tuple(string, string)) a list of tuples strings
    with zip code and state
    :param: destination_zip_state, tuple(string, string), a tuple of zip code and state as strings
    :param: commute_type, a string, either "driving", "transit", "walking", "biking"

    Example Input:
        origins = [("02123", "MA"), ("02012", Maine), ("12345", NY)]
        destination = ("20344", California)
        commute_type = "driving"
    """

    wrapper = DistanceWrapper(mode=commute_type)

    # map zip, state tuples list to a list of "zip state" strings
    results = wrapper.calculate_distances(list(map(lambda x:x[0]+" "+x[1], origins_zips_states)),
                                          [destination_zip_state[0]+" "+destination_zip_state[1]])

    # iterates both lists simultaneously
    for origin, result in zip(origins_zips_states, results):
        if ZipCodeDictionaryParentModel.objects.filter(zip_code_parent=origin[0]).exists():
            zip_code_dictionary = ZipCodeDictionaryParentModel.objects.get(zip_code_parent=origin[0])
            if zip_code_dictionary.zipcodedictionarychildmodel_set.filter(
                    zip_code_child=destination_zip_state[0],
                    commute_type_child=commute_type).exists():
                print("The combination that was computed already exists")
            else:
                zip_code_dictionary.zipcodedictionarychildmodel_set.create(
                    zip_code_child=destination_zip_state[0],
                    commute_type_child=commute_type,
                    commute_distance_meters_child=result[0][1],
                    commute_time_seconds_child=result[0][0],
                )
        else:
            ZipCodeDictionaryParentModel.objects.create(zip_code_parent=origin[0]) \
                .zipcodedictionarychildmodel_set.create(
                zip_code_child=destination_zip_state[0],
                commute_type_child=commute_type,
                commute_distance_meters_child=result[0][1],
                commute_time_seconds_child=result[0][0],
            )