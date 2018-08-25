# Django modules
from django import forms
from django.forms import ModelForm

# Survey models
from cocoon.survey.models import RentingSurveyModel, HomeInformationModel, CommuteInformationModel, RentingDestinationsModel, \
    PriceInformationModel, InteriorAmenitiesModel, ExteriorAmenitiesModel, DestinationsModel
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType

# Python global configurations
from config.settings.Global_Config import MAX_TEXT_INPUT_LENGTH, MAX_NUM_BEDROOMS, DEFAULT_RENT_SURVEY_NAME, \
    WEIGHT_QUESTION_MAX, MAX_NUM_BATHROOMS, HYBRID_WEIGHT_CHOICES, DEFAULT_COMMUTE_TYPE


class HomeInformationForm(ModelForm):
    num_bedrooms_survey = forms.ChoiceField(
        choices=[(x, x) for x in range(0, MAX_NUM_BEDROOMS)],
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

    def is_valid(self):
        valid = super(HomeInformationForm, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        if int(current_form['num_bedrooms_survey']) < 0:
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

    class Meta:
        model = HomeInformationModel
        fields = '__all__'


class PriceInformationForm(ModelForm):

    max_price_survey = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    desired_price_survey = forms.IntegerField(
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
                     HomeInformationForm):
    """
    Rent Survey is the rent survey on the main survey page
    """
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        exclude = ["user_profile_survey", 'survey_type_survey', "name_survey", ]


class RentSurveyFormMini(ExteriorAmenitiesForm, InteriorAmenitiesForm, PriceInformationForm,
                         HomeInformationForm):
    """
    RentSurveyFormMini is the survey that is on the survey results page and allows the user to create
    quick changes. This should be mostly a subset of the RentSurveyForm
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RentSurveyFormMini, self).__init__(*args, **kwargs)

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

    def is_valid(self):
        valid = super(RentSurveyFormMini, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        # Make sure the user cannot create a survey with the same name
        if self.user.userProfile.rentingsurveymodel_set.filter(name_survey=current_form['name_survey']).exists():
            self.add_error('name_survey', "Survey with that name already exists")
            valid = False

        return valid

    class Meta:
        model = RentingSurveyModel
        exclude = ["user_profile_survey", 'survey_type_survey']


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

    commute_type = forms.ModelChoiceField(
        queryset=CommuteType.objects.all(),
        label="Commute Type",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    class Meta:
        model = CommuteInformationModel
        fields = '__all__'


class DestinationForm(ModelForm):
    street_address = forms.CharField(
        label="Destination",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Street Address',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'City',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'State',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    zip_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Zip Code',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    class Meta:
        model = DestinationsModel
        fields = '__all__'


class RentingDestinationsForm(DestinationForm, CommuteInformationForm):

    class Meta:
        model = RentingDestinationsModel
        exclude = ['survey']
