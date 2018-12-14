# Import commutes models
from cocoon.commutes.models import ZipCodeBase, ZipCodeChild, CommuteType

# Constant value imports
from cocoon.commutes.constants import GoogleCommuteNaming, CommuteAccuracy

# Import DistanceWrapper
from .distance_wrapper import Distance_Matrix_Exception
from .commute_retriever import retrieve_exact_commute
from .home_cache import HomeCache

# Load the logger
import logging
logger = logging.getLogger(__name__)


def update_commutes_cache_rent_algorithm(homes, destinations, accuracy=CommuteAccuracy.DEFAULT):
    """
    This function updates the commute database for caching reasons. Therefore, this is the interface between
        the survey and the commutes to update any saved commute information
    :param homes: (list(HomeScore)) -> The homes that passed the static filter for the user
    :param destinations: (list(destinationModel)) -> The list of destinations that the user selected
    :param accuracy: (CommuteAccuracy) -> The accuracy type that is desire
    """

    # Since each destination can have a commute type, loop through all the destinations
    for destination in destinations:
        if destination.commute_type.commute_type == CommuteType.DRIVING:
            Driving(HomeCache.home_score_to_home_cache(homes), HomeCache.destination_to_home_cache(destination),
                    accuracy=accuracy).run()
        elif destination.commute_type.commute_type == CommuteType.TRANSIT:
            Transit(HomeCache.home_score_to_home_cache(homes), HomeCache.destination_to_home_cache(destination),
                    accuracy=accuracy).run()
        elif destination.commute_type.commute_type == CommuteType.BICYCLING:
            Bicycling(HomeCache.home_score_to_home_cache(homes), HomeCache.destination_to_home_cache(destination),
                      accuracy=accuracy).run()
        elif destination.commute_type.commute_type == CommuteType.WALKING:
            Walking(HomeCache.home_score_to_home_cache(homes), HomeCache.destination_to_home_cache(destination),
                    accuracy=accuracy).run()


def update_commutes_cache_client_scheduler(homes, destination, accuracy=CommuteAccuracy.DEFAULT, commute_type=CommuteType.DRIVING):

    if commute_type == CommuteType.DRIVING:
        Driving(HomeCache.rentdatabases_to_home_cache(homes), HomeCache.rentdatabase_to_home_cache(destination),
                accuracy=accuracy).run()
    elif commute_type == CommuteType.TRANSIT:
        Transit(HomeCache.rentdatabases_to_home_cache(homes), HomeCache.rentdatabase_to_home_cache(destination),
                accuracy=accuracy).run()
    elif commute_type == CommuteType.BICYCLING:
        Bicycling(HomeCache.rentdatabases_to_home_cache(homes), HomeCache.rentdatabase_to_home_cache(destination),
                  accuracy=accuracy).run()
    elif commute_type == CommuteType.WALKING:
        Walking(HomeCache.rentdatabases_to_home_cache(homes), HomeCache.rentdatabase_to_home_cache(destination),
                accuracy=accuracy).run()


class CommuteCalculator(object):
    """
    Base class that stores common information for the different commute types
    """

    def __init__(self, homes, destination, accuracy=CommuteAccuracy.DEFAULT):
        """
        Constructor for the base class
        :param homes: (list(HomeCache)) -> All the homes that the user can live at
        :param destination: (HomeCache) -> The current destination that is being computed
        :param accuracy: (CommuteAccuracy) -> The accuracy type desired
        """
        self.homes = homes
        self.destination = destination
        self.accuracy = accuracy


class Driving(CommuteCalculator):
    """
    This class updates the database to make sure it contains all the combinations necessary for storing
        the approximate zip codes
    """
    GOOGLE_COMMUTE_TYPE = GoogleCommuteNaming.DRIVING

    def __init__(self, homes, destination, accuracy=CommuteAccuracy.DEFAULT):
        super().__init__(homes, destination, accuracy=accuracy)
        self.COMMUTE_TYPE = CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0]

    def check_all_combinations(self):
        """
        This function checks every combination possible given multiple homes for a destination.
        Pairs that don't exist are passed to the generate_approximation_pair to create the pair in the database
        """
        failed_home_dict = dict()
        failed_list = self.find_missing_pairs(self.homes)

        # Add to the dictionary of failed homes
        failed_home_dict[(self.destination.zip_code, self.destination.state)] = failed_list

        # 2: Use approx handler to compute the failed home distances and update db
        for destination_zip, origin_list in failed_home_dict.items():
            try:
                self.generate_approximation_pair(origin_list, destination_zip)
            except Distance_Matrix_Exception as e:
                logger.warning("Caught: {0}".format(e.__class__.__name__))

    def find_missing_pairs(self, homes):
        """
        Given a list of homes, it determines if a zip_code pair exists between each home and destination.
            If not then it adds the pair to the failed list so the pair can be generated
        :param homes: (list[homeScore]) -> Homes that are being checked for zip-code pairs
        :return: (list[(string, string)] Returns a set of (zip_code, state) tuples of pairs that don't exist
            in the cache
        """
        # The reason a set is used is because this prevents adding duplicate entries because
        #   adding an entry that already exists does nothing
        failed_list = set()
        try:
            dest_zip = ZipCodeBase.objects.filter(zip_code__exact=self.destination.zip_code)

            # Generates a queryset of all the child zip_codes that exist for this destination
            child_zips = ZipCodeChild.objects.filter(base_zip_code=dest_zip). \
                filter(commute_type=self.COMMUTE_TYPE). \
                values_list('zip_code', 'last_date_updated')

            # Dictionary Compression to retrieve the values from the QuerySet
            child_zip_codes = {zip_code: last_update for zip_code, last_update in child_zips}

            # For every home, see if the home zip_code matches one of the zip_codes in the child_zip codes
            #   If not then add it to the failed_list
            for home in homes:

                # Determines if the home exists in the dictionary on child_zip_codes
                result = home.zip_code in child_zip_codes

                # If there is not pair or the pair is out of date then mark the pair as failed
                #   so it gets regenerated
                if not result or not ZipCodeChild.zip_code_cache_valid_check(child_zip_codes[home.zip_code]):
                    failed_list.add((home.zip_code, home.state))

        # If the ZipCodeBase doesn't exist then none of the children exist so add them all to the
        #   failed list
        except ZipCodeBase.DoesNotExist:
            for home in homes:
                failed_list.add((home.zip_code, home.state))

        return failed_list

    def generate_approximation_pair(self, origins_zips_states, destination_zip_state):
        """
        Generates the distance between two zip codes and adds it to the database (and deletes the old value
            if it is present)

        Note: There are two commutes names, the database commute name and the google distance matrix api commute name
        :param: origin_zips_states, list(tuple(string, string)) a list of tuples strings
        with zip code and state
        :param: destination_zip_state, tuple(string, string), a tuple of zip code and state as strings

        Example Input:
            origins = [("02123", "MA"), ("02012", Maine), ("12345", NY)]
            destination = ("20344", California)
            commute_type = "driving"
        """

        # map (zip, state) tuples list to a list of "state+zip" strings
        results = retrieve_exact_commute(list(map(lambda x: x[1] + "+" + x[0], origins_zips_states)),
                                         [destination_zip_state[1] + "+" + destination_zip_state[0]],
                                         self.COMMUTE_TYPE)

        if results:
            # iterates both lists simultaneously
            for origin, result in zip(origins_zips_states, results):
                if ZipCodeBase.objects.filter(zip_code=destination_zip_state[0]).exists():
                    zip_code_dictionary = ZipCodeBase.objects.get(zip_code=destination_zip_state[0])
                    zip_dest = zip_code_dictionary.zipcodechild_set.filter(
                        zip_code=origin[0],
                        commute_type=self.COMMUTE_TYPE)

                    # If the zip code doesn't exist or is not valid then compute the approximate distance
                    #   If the zip code was not valid then delete it first before recomputing it
                    if not zip_dest.exists() or not zip_dest.first().zip_code_cache_still_valid():
                        if zip_dest.exists():
                            zip_dest.delete()
                        zip_code_dictionary.zipcodechild_set.create(
                            zip_code=origin[0],
                            commute_type=self.COMMUTE_TYPE,
                            commute_distance_meters=result[0][1],
                            commute_time_seconds=result[0][0],
                        )
                else:
                    ZipCodeBase.objects.create(zip_code=destination_zip_state[0]) \
                        .zipcodechild_set.create(
                        zip_code=origin[0],
                        commute_type=self.COMMUTE_TYPE,
                        commute_distance_meters=result[0][1],
                        commute_time_seconds=result[0][0],
                    )

    def run_exact_commute_cache(self):
        pass

    def run(self):
        """
        The generic run method that each child class should have. Starts the execution of the class
        """
        if self.accuracy == CommuteAccuracy.EXACT:
            """
            Currently exact commutes are not stored in the database so nothing happens
            """
            self.run_exact_commute_cache()
        elif self.accuracy == CommuteAccuracy.APPROXIMATE:
            """
            If approximations are desired, then start the computation
            """
            self.check_all_combinations()
        else:
            logger.error("Undetermined accuracy type")


class Transit(Driving):
    """
    Currently Transit uses the same method as driving for caching. Therefore, just inherit
    all of the driving functionality. Later on the caching mechanism should be changed for transit
    """
    GOOGLE_COMMUTE_TYPE = GoogleCommuteNaming.TRANSIT

    def __init__(self, homes, destination, accuracy=CommuteAccuracy.DEFAULT):
        super().__init__(homes, destination, accuracy=accuracy)
        self.COMMUTE_TYPE = CommuteType.objects.get_or_create(commute_type=CommuteType.TRANSIT)[0]


class Bicycling(CommuteCalculator):
    """
    Currently the approximation for biking is done via the lat, long distance and therefore,
        do not have to be saved.
    """
    GOOGLE_COMMUTE_TYPE = GoogleCommuteNaming.BICYCLING

    def __init__(self, homes, destination, accuracy=CommuteAccuracy.DEFAULT):
        super().__init__(homes, destination, accuracy=accuracy)
        self.COMMUTE_TYPE = CommuteType.objects.get_or_create(commute_type=CommuteType.BICYCLING)[0]

    def run(self):
        pass


class Walking(CommuteCalculator):
    """
    Currently the approximation for walking is done via the lat, long distance and therefore,
        do not have to be saved.
    """
    GOOGLE_COMMUTE_TYPE = GoogleCommuteNaming.WALKING

    def __init__(self, homes, destination, accuracy=CommuteAccuracy.DEFAULT):
        super().__init__(homes, destination, accuracy=accuracy)
        self.COMMUTE_TYPE = CommuteType.objects.get_or_create(commute_type=CommuteType.WALKING)[0]

    def run(self):
        pass
