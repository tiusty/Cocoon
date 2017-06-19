from enum import Enum

# Survey Global Variables
default_buy_survey_name = "Recent Buy Survey"
default_rent_survey_name = "Recent Rent Survey"

survey_types = Enum('survey_types', 'rent buy')

# Default Survey Max Values
weight_question_value = 20
weight_question_max = 7
Max_Num_Bathrooms = 7  # Base 0, I guess should be base 1
Max_Num_Bedrooms = 6  # Base 1, so from 1 bedroom to 6 bedrooms
Max_Text_Input_Length = 200
Hybrid_weighted_max = 3
Hybrid_weighted_min = -3

# Survey preferences
# This is the acceptable range for an apartment. So if the user selected a commute of 30 - 60 minutes
# Homes with a commute of 10-80 will be accepted. This is to account for the difference of commute
# within a given zip code
approximate_commute_range = 20
