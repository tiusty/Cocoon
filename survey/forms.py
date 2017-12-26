# Django modules
from django import forms
from django.forms import ModelForm
from django.db.models import Q

# Python Modules
import datetime

# Survey models
from survey.models import RentingSurveyModel, RentingDestinations, HomeTypeModel

# Python global configurations
from Unicorn.settings.Global_Config import MAX_TEXT_INPUT_LENGTH, MAX_NUM_BEDROOMS, DEFAULT_RENT_SURVEY_NAME, \
    WEIGHT_QUESTION_MAX, MAX_NUM_BATHROOMS, COMMUTE_TYPES, HYBRID_WEIGHT_CHOICES


class HomeInformationForm(ModelForm):

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
        choices=[(x, x) for x in range(1, MAX_NUM_BEDROOMS)],
        label="Number of Bedrooms",
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

    home_type = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }),
        # Prevents other objects from being displayed as choices as a home type,
        # If more home_types are added then it needs to be added here to the survey
        queryset=HomeTypeModel.objects.filter(Q(home_type_survey__startswith="House")
                                              | Q(home_type_survey__startswith="Apartment")
                                              | Q(home_type_survey__startswith="Condo")
                                              | Q(home_type_survey__startswith="Town House"))
    )

    def is_valid(self):
        valid = super(HomeInformationForm, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        # Validate move-in field
        if current_form['move_in_date_start'] < datetime.date.today():
            self.add_error('move_in_date_start', "Start Day should not be in the past")
            valid = False

        # Makes sure that the End day is after the start day
        if current_form['move_in_date_start'] > current_form['move_in_date_end']:
            self.add_error('move_in_date_end', "End date should not be before the start date")
            valid = False

        if int(current_form['num_bedrooms']) < 1:
            self.add_error('num_bedrooms', "There can't be less than 1 bedroom")
            valid = False

        # Make sure the bedrooms are not more than the max allowed
        if int(current_form['num_bedrooms']) > MAX_NUM_BEDROOMS:
            self.add_error('num_bedrooms', "There can't be more than " + str(MAX_NUM_BEDROOMS))
            valid = False

        # make sure that the max number of bathrooms is not greater than the max specified
        if current_form['max_bathrooms'] > MAX_NUM_BATHROOMS:
            self.add_error('max_bathrooms', "You can't have more bathrooms than " + str(MAX_NUM_BATHROOMS))
            valid = False

        if current_form['min_bathrooms'] < 0:
            self.add_error('min_bathrooms', "You can't have less than 0 bathrooms")
            valid = False

        return valid


class CommuteInformationForm(ModelForm):

    max_commute = forms.IntegerField(
        widget=forms.HiddenInput(
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

    commute_weight = forms.ChoiceField(
        choices=[(x, x) for x in range(0, WEIGHT_QUESTION_MAX)],
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

    def is_valid(self):
        valid = super(CommuteInformationForm, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        if int(current_form['commute_weight']) > WEIGHT_QUESTION_MAX:
            self.add_error('commute_weight', "Commute weight cant' be greater than " + str(WEIGHT_QUESTION_MAX))
            valid = False

        if int(current_form['commute_weight']) < 0:
            self.add_error('commute_weight', "Commute weight cant' be less than 0")
            valid = False

        return valid


class PriceInformationForm(ModelForm):

    max_price = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    min_price = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    price_weight = forms.ChoiceField(
        choices=[(x, x) for x in range(0, WEIGHT_QUESTION_MAX)],
        label="Price Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )


class InteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields in regards to the interior Amenities
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


class ExteriorAmenitiesForm(ModelForm):
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


class RentSurvey(ExteriorAmenitiesForm, InteriorAmenitiesForm, PriceInformationForm,
                 CommuteInformationForm, HomeInformationForm):
    """
    Rent Survey is the rent survey on the main survey page
    """
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        exclude = ["user_profile", 'survey_type', 'name', ]


class RentSurveyMini(ExteriorAmenitiesForm, InteriorAmenitiesForm, PriceInformationForm,
                     CommuteInformationForm, HomeInformationForm):
    """
    RentSurveyMini is the survey that is on the survey results page and allows the user to create
    quick changes. This should be mostly a subset of the RentSurvey
    """
    name = forms.CharField(
        label="Survey Name",
        initial=DEFAULT_RENT_SURVEY_NAME,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of the survey',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    class Meta:
        model = RentingSurveyModel
        exclude = ["user_profile", 'survey_type']


class DestinationForm(ModelForm):
    street_address = forms.CharField(
        label="Destination",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter in a Destination',
                'autocomplete': 'off',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the city',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the State',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    zip_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Zip Code',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    class Meta:
        model = RentingDestinations
        fields = '__all__'
