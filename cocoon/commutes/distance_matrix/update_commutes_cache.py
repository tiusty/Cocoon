# Import commutes models
from cocoon.commutes.models import ZipCodeBase, ZipCodeChild

# Constant value imports
from cocoon.commutes.constants import GoogleCommuteNaming, CommuteAccuracy

# Import DistanceWrapper
from cocoon.commutes.distance_matrix.distance_wrapper import Distance_Matrix_Exception
from cocoon.commutes.distance_matrix import compute_approximates

# Load the logger
import logging
logger = logging.getLogger(__name__)


def update_commutes_cache(homes, destinations, accuracy=CommuteAccuracy.DEFAULT):
    """
    This function updates the commute database for caching reasons. Therefore, this is the interface between
        the survey and the commutes to update any saved commute information
    :param homes: (list(HomeScore)) -> The homes that passed the static filter for the user
    :param destinations: (list(destinationModel)) -> The list of destinations that the user selected
    :param accuracy: (CommuteAccuracy) -> The accuracy type that is desire
    """

    # Since each destination can have a commute type, loop through all the destinations
    for destination in destinations:
        if destination.commute_type == GoogleCommuteNaming.DRIVING:
            Driving(homes, destination, accuracy=accuracy).run()
        elif destination.commute_type == GoogleCommuteNaming.TRANSIT:
            Transit(homes, destination, accuracy=accuracy).run()
        elif destination.commute_type == GoogleCommuteNaming.BICYCLING:
            Bicycling(homes, destination, accuracy=accuracy).run()
        elif destination.commute_type == GoogleCommuteNaming.WALKING:
            Walking(homes, destination, accuracy=accuracy).run()
        else:
            logger.error("Unknown commute_type: {0}".format(destination.commute_type))


class CommuteCalculator(object):
    """
    Base class that stores common information for the different commute types
    """

    def __init__(self, homes, destination, accuracy=CommuteAccuracy.DEFAULT):
        """
        Constructor for the base class
        :param homes: (list(home_score)) -> All the homes that the user can live at
        :param destination: (DestinationModel) -> The current destination that is being computed
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

    def check_all_combinations(self):
        """
        This function checks every combination possible given multiple homes for a destination.
        If a pair doesn't exist, it will add the pair to a list and then at the end compute the
        approximation for the missing pairs
        """
        failed_home_dict = dict()
        failed_list = []
        for home_score in self.homes:
            if not self.does_pair_exist(home_score.home):
                failed_list.append((home_score.home.zip_code, home_score.home.state))

        # Add to the dictionary of failed homes
        failed_home_dict[(self.destination.zip_code, self.destination.state)] = failed_list

        # 2: Use approx handler to compute the failed home distances and update db
        for destination_zip, origin_list in failed_home_dict.items():
            try:
                compute_approximates.approximate_commute_handler(origin_list, destination_zip,
                                                                 self.destination.commute_type)
            except Distance_Matrix_Exception as e:
                logger.warning("Caught: {0}".format(e.__class__.__name__))

    def does_pair_exist(self, home):
        """
        This function given a pair of locations, checks to see if the combination exists in the cache already.
        If it does, then the cache doesn't need to be added, if it doesn't, then it returns false.
        It also does a check to see how old the pair is, and if it is too old, then it will return false.
        :param home: (homeScore) -> The home that is being computed
        """
        parent_zip_code_dictionary = ZipCodeBase.objects.filter(zip_code__exact=home.zip_code)
        if parent_zip_code_dictionary.exists():
            for parent in parent_zip_code_dictionary:
                zip_code_dictionary = ZipCodeChild.objects.filter(
                    base_zip_code_id=parent).filter(zip_code__exact=self.destination.zip_code) \
                    .filter(commute_type=self.destination.commute_type)
                if zip_code_dictionary.exists():
                    for match in zip_code_dictionary:
                        if match.zip_code_cache_still_valid():
                            return True
                        else:
                            return False
                else:
                    return False
        else:
            return False

    def run(self):
        """
        The generic run method that each chlid class should have. Starts the execution of the class
        """
        if self.destination.commute_type == CommuteAccuracy.EXACT:
            """
            Currently exact commutes are not stored in the database so nothing happens
            """
            pass
        elif self.destination.commute_type == CommuteAccuracy.APPROXIMATE:
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
    pass


class Bicycling(CommuteCalculator):
    """
    Currently the approximation for biking is done via the lat, long distance and therefore,
        do not have to be saved.
    """
    def run(self):
        pass


class Walking(CommuteCalculator):
    """
    Currently the approximation for walking is done via the lat, long distance and therefore,
        do not have to be saved.
    """

    def run(self):
        pass
