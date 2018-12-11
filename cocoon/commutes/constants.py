from enum import Enum
import datetime
import time

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

curr_year = 2019
traffic_date = datetime.date(curr_year, 12, 4)
with_traffic_time = datetime.time(16, 30) # 4:30pm
without_traffic_time = datetime.time(3, 30) # 3:30am

commute_time_traffic_temp = datetime.datetime.combine(traffic_date, with_traffic_time)
commute_time_no_traffic_temp = datetime.datetime.combine(traffic_date, without_traffic_time)
# Check if your commute time is in the future, if it is then change both times by a increasing it
# a year, this makes sure that the time is always in the future

if (commute_time_no_traffic_temp - datetime.datetime.now()).seconds <= 0 or \
        (commute_time_traffic_temp - datetime.datetime.now()).seconds <= 0:
    curr_year += 1
    traffic_date = datetime.date(curr_year, 12, 4)

COMMUTE_TIME_WITH_TRAFFIC = datetime.datetime.combine(traffic_date, with_traffic_time)
COMMUTE_TIME_WITHOUT_TRAFFIC = datetime.datetime.combine(traffic_date, without_traffic_time)
TRAFFIC_MODEL_DEFAULT = "best_guess"

