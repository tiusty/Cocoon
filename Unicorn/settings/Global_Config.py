from enum import Enum

# Survey Global Variables
default_buy_survey_name = "Recent Buy Survey"
default_rent_survey_name = "Recent Rent Survey"

survey_types = Enum('survey_types', 'rent buy')

# Default Survey Max Values
weight_question_value = 20
Max_Num_Bathrooms = 7
Commute_Range_Max_Scale = 6  # Remember base 0, so value of 6 is 0-5
Num_Bedrooms_Max = 6  # Base 1, so from 1 bedroom to 6 bedrooms
Max_Num_Bathrooms = 7
Max_Text_Input_Length = 200
Hybrid_weighted_max = 7
