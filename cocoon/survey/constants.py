# This is the price in dollars that the minimum price is bellow the desired price
#   The user does not set the minimum price so we arbitrarily set it for tham.
MIN_PRICE_DELTA = 300

# Number of homes that have exact commutes computed in the survey
NUMBER_OF_EXACT_COMMUTES_COMPUTED = 45

# Number of homes returned with the survey results
NUMBER_OF_HOMES_RETURNED = 35

# Number of minutes that is allowed for the approximation
APPROX_COMMUTE_RANGE = 20

# Survey weight values
COMMUTE_QUESTION_WEIGHT = 100
HYBRID_QUESTION_WEIGHT = 20
PRICE_WEIGHT_QUESTION = 100
WEIGHT_QUESTION_MAX = 6
HYBRID_WEIGHT_MAX = 3
HYBRID_WEIGHT_MIN = 0

HYBRID_WEIGHT_CHOICES = (
    (3, "Must have"),
    (2, "Really want"),
    (1, "Prefer to have"),
    (0, "I don't care"),
    (-1, "Prefer not to have"),
    (-2, "Really don't want"),
    (-3, "Don't want"),
)

# Commute range
MAX_COMMUTE_TIME = 180
MIN_COMMUTE_TIME = 10

# Average walking speed in mph
AVERAGE_WALKING_SPEED = 3

# Average bicycling speed in mph
AVERAGE_BICYCLING_SPEED = 10

# extra distance to add to take into account going around roads and rivers
EXTRA_DISTANCE_LAT_LNG_APPROX = 4  # In miles

# The maximum number of people for a single survey, not including 5, so
#   this means up to 4 tenants allowed
MAX_TENANTS_FOR_ONE_SURVEY = 5
