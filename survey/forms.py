# Django modules
from django import forms
from django.forms import ModelForm
from django.utils import timezone

# Survey models
from survey.models import RentingSurveyModel, HomeInformationModel, CommuteInformationModel, RentingDestinations, \
    PriceInformationModel, InteriorAmenitiesModel, ExteriorAmenitiesModel
from houseDatabase.models import HomeTypeModel

# Python global configurations
from Unicorn.settings.Global_Config import MAX_TEXT_INPUT_LENGTH, MAX_NUM_BEDROOMS, DEFAULT_RENT_SURVEY_NAME, \
    WEIGHT_QUESTION_MAX, MAX_NUM_BATHROOMS, COMMUTE_TYPES, HYBRID_WEIGHT_CHOICES


class HomeInformationForm(ModelForm):

    move_in_date_start_survey = forms.DateField(
        label="Start of move in range",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose first day to move in',
            },
            format='%m/%d/%Y',
        ))

    move_in_date_end_survey = forms.DateField(
        label="End of move in range",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Choose last date to move in',
            },
            format='%m/%d/%Y',
        ))

    num_bedrooms_survey = forms.ChoiceField(
        choices=[(x, x) for x in range(1, MAX_NUM_BEDROOMS)],
        label="Number of Bedrooms",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    max_bathrooms_survey = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    min_bathrooms_survey = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    home_type_survey = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }),
        queryset=HomeTypeModel.objects.all()
    )

    @property
    def move_in_date_start(self):
        return self.move_in_date_start_survey

    @property
    def move_in_date_end(self):
        return self.move_in_date_end_survey

    @property
    def num_bedrooms(self):
        return self.num_bedrooms_survey

    @property
    def min_bathrooms(self):
        return self.min_bathrooms_survey

    @property
    def max_bathrooms(self):
        return self.max_bathrooms_survey

    def is_valid(self):
        valid = super(HomeInformationForm, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        # Validate move-in field
        if current_form['move_in_date_start_survey'] < timezone.now().date():
            self.add_error('move_in_date_start_survey', "Start Day should not be in the past")
            valid = False

        # Makes sure that the End day is after the start day
        if current_form['move_in_date_start_survey'] > current_form['move_in_date_end_survey']:
            self.add_error('move_in_date_end_survey', "End date should not be before the start date")
            valid = False

        if int(current_form['num_bedrooms_survey']) < 1:
            self.add_error('num_bedrooms_survey', "There can't be less than 1 bedroom")
            valid = False

        # Make sure the bedrooms are not more than the max allowed
        if int(current_form['num_bedrooms_survey']) > MAX_NUM_BEDROOMS:
            self.add_error('num_bedrooms_survey', "There can't be more than " + str(MAX_NUM_BEDROOMS))
            valid = False

        # make sure that the max number of bathrooms is not greater than the max specified
        if current_form['max_bathrooms_survey'] > MAX_NUM_BATHROOMS:
            self.add_error('max_bathrooms_survey', "You can't have more bathrooms than " + str(MAX_NUM_BATHROOMS))
            valid = False

        if current_form['min_bathrooms_survey'] < 0:
            self.add_error('min_bathrooms_survey', "You can't have less than 0 bathrooms")
            valid = False

        return valid

    @property
    def move_in_data_start(self):
        return self.move_in_date_start_survey

    class Meta:
        model = HomeInformationModel
        fields = '__all__'


class CommuteInformationForm(ModelForm):

    max_commute_survey = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    min_commute_survey = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    commute_weight_survey = forms.ChoiceField(
        choices=[(x, x) for x in range(0, WEIGHT_QUESTION_MAX)],
        label="Commute Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    commute_type_survey = forms.ChoiceField(
        choices=COMMUTE_TYPES,
        label="Commute Type",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    @property
    def commute_type(self):
        return self.commute_type_survey

    class Meta:
        model = CommuteInformationModel
        fields = '__all__'


class PriceInformationForm(ModelForm):

    max_price_survey = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    min_price_survey = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    price_weight_survey = forms.ChoiceField(
        choices=[(x, x) for x in range(0, WEIGHT_QUESTION_MAX)],
        label="Price Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    @property
    def min_price(self):
        return self.min_price_survey

    @property
    def max_price(self):
        return self.max_price_survey

    class Meta:
        model = PriceInformationModel
        fields = '__all__'


class InteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields in regards to the interior Amenities
    """

    air_conditioning_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Air conditioning",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    interior_washer_dryer_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Wash + Dryer in Home",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    dish_washer_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Dish Washer",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    bath_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Bath",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = InteriorAmenitiesModel
        fields = '__all__'


class ExteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the BuildingExteriorAmenitiesModel Model
    """
    parking_spot_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Parking Spot",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    building_washer_dryer_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Washer/Dryer in Building",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    elevator_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Elevator",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    handicap_access_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Handicap Access",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    pool_hot_tub_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Pool/Hot tub",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    fitness_center_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Fitness Center",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    storage_unit_survey = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Storage Unit",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = ExteriorAmenitiesModel
        fields = '__all__'


class RentSurveyForm(ExteriorAmenitiesForm, InteriorAmenitiesForm, PriceInformationForm,
                     CommuteInformationForm, HomeInformationForm):
    """
    Rent Survey is the rent survey on the main survey page
    """
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        exclude = ["user_profile_survey", 'survey_type_survey', "name_survey", ]


class RentSurveyFormMini(ExteriorAmenitiesForm, InteriorAmenitiesForm, PriceInformationForm,
                         CommuteInformationForm, HomeInformationForm):
    """
    RentSurveyFormMini is the survey that is on the survey results page and allows the user to create
    quick changes. This should be mostly a subset of the RentSurveyForm
    """
    name_survey = forms.CharField(
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
        exclude = ["user_profile_survey", 'survey_type_survey']


class DestinationForm(ModelForm):
    street_address_destination = forms.CharField(
        label="Destination",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter in a Destination',
                'autocomplete': 'off',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    city_destination = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the city',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    state_destination = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the State',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    zip_code_destination = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Zip Code',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    class Meta:
        model = RentingDestinations
        exclude = ['survey_destinations']
