from enum import Enum

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


# Traffic Mode Constants- Note: This needs to be updated every year
# API does not accept times from the past
# With traffic = Tuesday Dec 4, 2019 4:30pm
# Without traffic = Tuesday Dec 4, 2019 3:30am
COMMUTE_TIME_WITH_TRAFFIC = 1575477036
COMMUTE_TIME_WITHOUT_TRAFFIC = 1575430236
TRAFFIC_MODEL_DEFAULT = "best_guess"