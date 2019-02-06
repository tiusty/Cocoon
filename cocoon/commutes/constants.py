from enum import Enum
from datetime import time

# Controls how many days until the zip codes need to be refreshed
ZIP_CODE_TIMEDELTA_VALUE = 60


# Google Distance Matrix Api naming convention
class GoogleCommuteNaming:
    DRIVING = "driving"
    TRANSIT = "transit"
    BICYCLING = "bicycling"
    WALKING = "walking"
    DEFAULT = DRIVING


# Enum to determine which accuracy is desired for commutes
class CommuteAccuracy(Enum):
    APPROXIMATE = 1
    EXACT = 2
    DEFAULT = EXACT


# The times that the with traffic and without traffic is computed with

# Since the commutes are computed from the work to the home, this correspondes to the afternoon commute.
#   Therefore, for accurate commute info, the departure time should be in the afternoon and not the morning
COMMUTE_TIME_WITH_TRAFFIC = time(17, 0)
COMMUTE_TIME_WITHOUT_TRAFFIC = time(3, 30)

# Traffic model
TRAFFIC_MODEL_PESSIMISTIC = "pessimistic"
TRAFFIC_MODEL_BEST_GUESS = "best_guess"
