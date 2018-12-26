from enum import Enum
import datetime

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


# This expression always results in a tuesday in the third week of january, on the next year from today
d = datetime.date(datetime.datetime.today().year + 1 , 1, 4)
d = d + datetime.timedelta(weeks=2, days=-d.weekday()+1)

# 5:30pm for traffic
# 3:30am for no-traffic
COMMUTE_TIME_WITH_TRAFFIC = datetime.datetime.combine(d, datetime.time(7, 30)).timestamp()
COMMUTE_TIME_WITHOUT_TRAFFIC = datetime.datetime.combine(d, datetime.time(3, 30)).timestamp()
TRAFFIC_MODEL_DEFAULT = "best_guess"
