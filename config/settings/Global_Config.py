from enum import Enum
import googlemaps

# Survey Global Variables
default_buy_survey_name = "Recent Buy Survey"
DEFAULT_RENT_SURVEY_NAME = "Recent Rent Survey"

survey_types = Enum('survey_types', 'rent buy')


# Default Survey Max Values
MAX_NUM_BATHROOMS = 7  # Base 0, I guess should be base 1
MAX_NUM_BEDROOMS = 6  # Base 0, so from 0 bedroom to 6 bedrooms, 0 bedrooms means studio
MAX_TEXT_INPUT_LENGTH = 200

# Survey preferences
# This is the acceptable range for an apartment. So if the user selected a commute of 30 - 60 minutes
# Homes with a commute of 10-80 will be accepted. This is to account for the difference of commute
# within a given zip code

# Google distance matrix values
gmaps_api_key = 'AIzaSyCayNcf_pxLj5vaOje1oXYEMIQ6H53Jzho'
gmaps = googlemaps.Client(key=gmaps_api_key)
