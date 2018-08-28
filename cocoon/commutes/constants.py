from enum import Enum

# Controls how many days until the zip codes need to be refreshed
ZIP_CODE_TIMEDELTA_VALUE = 60


# Google Distance Matrix Api naming convention
class GoogleCommuteNaming:
    DRIVING = "Driving"
    TRANSIT = "Transit"
    BICYCLING = "Bicycling"
    WALKING = "Walking"
    DEFAULT = DRIVING


# Enum to determine which accuracy is desired for commutes
class CommuteAccuracy(Enum):
    APPROXIMATE = 1
    EXACT = 2
    DEFAULT = EXACT


