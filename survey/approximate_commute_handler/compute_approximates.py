from houseDatabase.models import RentDatabaseModel, HomeTypeModel, ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel
from survey.distance_matrix.distance_wrapper import DistanceWrapper

#TODO: how are we handling problems associated with passing only zip code
#TODO: should we still update zip codes after certain period of time

"""
uses the distanc_wrapper to poll the distance matrix API, creating 
parent-child zip code objects to store the results in the database.

:param: origins, the list of origin zip codes
:param: destination, the destination zip code
:param: commute type
"""
def approximate_compute_handler(origins, destination, commute_type):
    wrapper = DistanceWrapper()

    # list of lists of tuples
    # each inner lists corresponds to an origin
    # each tuple corresponds to a origin-destination combo
    results = wrapper.calculate_distances(origins, [destination])

    # iterates both lists
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