from houseDatabase.models import RentDatabaseModel, HomeTypeModel, ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel
from survey.distance_matrix.distance_wrapper import DistanceWrapper

"""
uses the distanc_wrapper to poll the distance matrix API, creating 
parent-child zip code objects to store the results in the database.

:param: origins, the list of origin zip codes
:param: destination, the destination zip code
"""
def approximate_compute_handler(origins, destination):
    wrapper = DistanceWrapper()

    # list of lists of tuples
    # each inner lists corresponds to an origin
    # each tuple corresponds to a origin-destination combo
    results = wrapper.calculate_distances(origins, destination)

    # iterates both lists
    for origin, result in zip(origins, results):
        '''
        check if parent exists
        if it doesn't create it 
            create the child 
            set its properties
        if it doesn't 
            check if the child exists
            if it doesn't, create it 
                set its props
            if it does, update its props
        
        '''
        try:
            parent_zip_dict = ZipCodeDictionaryParentModel.objects.get(zip_code=origin)
            try:
                child_zip = ZipCodeDictionaryChildModel.
        except: