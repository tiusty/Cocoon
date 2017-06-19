from django import forms
from survey.models import RentingSurveyModel, RentingDestinations, HomeType, COMMUTE_TYPES, HYBRID_WEIGHT_CHOICES
from django.forms import ModelForm
from django.db.models import Q
import datetime

# Python global configurations
from Unicorn.settings.Global_Config import \
    Max_Num_Bathrooms, Max_Text_Input_Length, \
    Max_Num_Bedrooms, default_rent_survey_name, \
    weight_question_max


class DestinationForm(ModelForm):
    street_address = forms.CharField(
        label="Destination",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter in a Destination',
                'autocomplete': 'off',
            }),
        max_length=Max_Text_Input_Length,
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the city',
            }),
        max_length=Max_Text_Input_Length,
    )

    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the State',
            }),
        max_length=Max_Text_Input_Length,
    )

    zip_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Zip Code',
            }),
        max_length=Max_Text_Input_Length,
    )

    class Meta:
        model = RentingDestinations
        fields = ["street_address", 'city', 'state', 'zip_code']


class RentSurveyBase(ModelForm):
    # if name is left blank it sets a default name
    min_price = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    max_price = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    price_weight = forms.ChoiceField(
        choices=[(x, x) for x in range(0, weight_question_max)],
        label="Price Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    min_commute = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    max_commute = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    home_type = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }),
        # Prevents other objects from being displayed as choices as a home type,
        # If more hometypes are added then it needs to be added here to the survey
        queryset=HomeType.objects.filter(Q(homeType__startswith="House")
                                         | Q(homeType__startswith="Apartment")
                                         | Q(homeType__startswith="Condo")
                                         | Q(homeType__startswith="Town House"))
    )

    commute_weight = forms.ChoiceField(
        choices=[(x, x) for x in range(0, weight_question_max)],
        label="Commute Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    commute_type = forms.ChoiceField(
        choices=COMMUTE_TYPES,
        label="Commute Type",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    move_in_date_start = forms.DateField(
        label="Start of move in range",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose first day to move in',
            },
            format='%m/%d/%Y',
        ))

    move_in_date_end = forms.DateField(
        label="End of move in range",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose last date to move in',
            },
            format='%m/%d/%Y',
        ))

    num_bedrooms = forms.ChoiceField(
        choices=[(x, x) for x in range(1, Max_Num_Bedrooms)],
        label="Number of Bedrooms",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    # Adding validation constraints to form
    # Need to make sure the move in day is properly set
    # Aka the start date is before the end date
    def is_valid(self):
        valid = super(RentSurveyBase, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        # Validate all the form fields

        # Makes sure the start date is either the present day or in the future
        if current_form['move_in_date_start'] < datetime.date.today():
            self.add_error('move_in_date_start', "Start Day should not be in the past")
            valid = False

        # Makes sure that the End day is after the start day
        if current_form['move_in_date_start'] > current_form['move_in_date_end']:
            self.add_error('move_in_date_end', "End date should not be before the start date")
            valid = False

        # Make sure that the minimum number of bathrooms is not less then 0
        if current_form['min_bathrooms'] < 0:
            self.add_error('min_bathrooms', "You can't have less than 0 bathrooms")
            valid = False

        # make sure that the max number of bathrooms is not greater than the max specified
        if current_form['max_bathrooms'] > Max_Num_Bathrooms:
            self.add_error('max_bathrooms', "You can't have more bathrooms than " + str(Max_Num_Bathrooms))
            valid = False

        # Make sure the bedrooms is at least 1
        # With the choice fields, the field needs to be casted as an int since it
        # Is stored as a string in cleaned_data
        if int(current_form['num_bedrooms']) < 1:
            self.add_error('num_bedrooms', "There can't be less than 1 bedroom")
            valid = False

        # Make sure the bedrooms are not more than the max allowed
        if int(current_form['num_bedrooms']) > Max_Num_Bedrooms:
            self.add_error('num_bedrooms', "There can't be more than " + str(Max_Num_Bedrooms))
            valid = False

        # Make sure
        if int(current_form['commute_weight']) > weight_question_max:
            self.add_error('commute_weight', "Commute weight cant' be greater than " + str(weight_question_max))
            valid = False

        if int(current_form['commute_weight']) < 0:
            self.add_error('commute_weight', "Commute weight cant' be less than 0")
            valid = False

        return valid


class InteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields in regards to the interior Admenities
    """

    air_conditioning = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Air conditioning",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    wash_dryer_in_home = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Wash + Dryer in Home",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    dish_washer = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Dish Washer",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    bath = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Bath",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    max_bathrooms = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    min_bathrooms = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )


class BuildingExteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the BuildingExteriorAmenities Model
    """
    parking_spot = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Parking Spot",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    washer_dryer_in_building = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Washer/Dryer in Building",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    elevator = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Elevator",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    handicap_access = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Handicap Access",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    pool_hot_tub = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Pool/Hot tub",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    fitness_center = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Fitness Center",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    storage_unit = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Storage Unit",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )


class RentSurvey(RentSurveyBase, InteriorAmenitiesForm, BuildingExteriorAmenitiesForm):
    """
    Rent Survey is the rent survey on the main survey page
    """
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        exclude = ["user_profile", 'survey_type', 'name', ]


class RentSurveyMini(RentSurveyBase, InteriorAmenitiesForm, BuildingExteriorAmenitiesForm):
    """
    RentSurveyMini is the survey that is on the survey results page and allows the user to create
    quick changes. This should be mostly a subset of the RentSurvey
    """
    name = forms.CharField(
        label="Survey Name",
        initial=default_rent_survey_name,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of the survey',
            }),
        max_length=Max_Text_Input_Length,
    )

    class Meta:
        model = RentingSurveyModel
        exclude = ["user_profile", 'survey_type']


# class BuySurvey(ModelForm):
#     class Meta:
#         model = BuyingSurveyModel
#         fields = ['maxPrice', ]
