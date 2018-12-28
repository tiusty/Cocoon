from enum import Enum
import datetime
from dateutil import tz

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
d = datetime.date(datetime.datetime.today().year + 1, 1, 4)
d = d + datetime.timedelta(weeks=2, days=-d.weekday()+1)

# 4:30pm for traffic because the origin of the commute is the destination they want to go to, so it would
#   be the afternoon commute
# 3:30am for no-traffic
# Right now we only support Boston so the timezone for the commute should be based on EST
NYC = tz.gettz('America/New_York')
COMMUTE_TIME_WITH_TRAFFIC = datetime.datetime.combine(d, datetime.time(17, 0)).replace(tzinfo=NYC).timestamp()
COMMUTE_TIME_WITHOUT_TRAFFIC = datetime.datetime.combine(d, datetime.time(3, 30)).replace(tzinfo=NYC).timestamp()

# Traffic model
TRAFFIC_MODEL_PESSIMISTIC = "pessimistic"
TRAFFIC_MODEL_BEST_GUESS = "best_guess"
