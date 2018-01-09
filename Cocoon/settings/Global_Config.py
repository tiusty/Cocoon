from enum import Enum
import googlemaps

# Survey Global Variables
default_buy_survey_name = "Recent Buy Survey"
DEFAULT_RENT_SURVEY_NAME = "Recent Rent Survey"

survey_types = Enum('survey_types', 'rent buy')

# House Database config values
COMMUTE_TYPES = (
    ('driving', 'Driving'),
    ('transit', 'Transit'),
    ('walking', 'Walking'),
    ('biking', 'Biking'),
)
ZIP_CODE_TIMEDELTA_VALUE = 60

# Default Survey Max Values
HYBRID_QUESTION_WEIGHT = 20
commute_question_weight = 100
price_question_weight = 100
WEIGHT_QUESTION_MAX = 7
MAX_NUM_BATHROOMS = 7  # Base 0, I guess should be base 1
MAX_NUM_BEDROOMS = 6  # Base 1, so from 1 bedroom to 6 bedrooms
MAX_TEXT_INPUT_LENGTH = 200
HYBRID_WEIGHT_MAX = 3
HYBRID_WEIGHT_MIN = -3
HYBRID_WEIGHT_CHOICES = (
    (3, "Must have"),
    (2, "Really want"),
    (1, "Prefer to have"),
    (0, "I don't care"),
    (-1, "Prefer not to have"),
    (-2, "Really don't want"),
    (-3, "Don't want"),
)

# Survey preferences
# This is the acceptable range for an apartment. So if the user selected a commute of 30 - 60 minutes
# Homes with a commute of 10-80 will be accepted. This is to account for the difference of commute
# within a given zip code
approximate_commute_range = 20
number_of_exact_commutes_computed = 100 # number of homes that the exact commute is calculated

# Google distance matrix values
gmaps = googlemaps.Client(key='AIzaSyDpV0VIEDoBzbflBgr506-udNqSLd127aw')


# Key:

# User Registration Data
creation_key_value = "cocoon2017usercreation"
