from django import forms
from survey.models import RentingSurveyModel, BuyingSurveyModel, RentingDesintations, HomeType, default_rent_survey_name
from django.forms import ModelForm
from django.db.models import Q

# Python global configurations
Commute_Range_Max_Scale = 6  # Remember base 0, so value of 6 is 0-5
Num_Bedrooms_Max = 6  # Base 1, so from 1 bedroom to 6 bedrooms
Max_Text_Input_Length = 200
Hybrid_weighted_max = 7


class DestinationForm(ModelForm):
    streetAddress = forms.CharField(
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
        model = RentingDesintations
        fields = ['streetAddress', 'city', 'state', 'zip_code']


class RentSurveyBase(ModelForm):
    #if name is left blank it sets a default name
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
    minPrice = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    maxPrice = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    minCommute = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    maxCommute = forms.IntegerField(
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
        queryset=HomeType.objects.filter(Q(homeType__startswith="house")
                                         | Q(homeType__startswith="Apartment")
                                         | Q(homeType__startswith="condo")
                                         | Q(homeType__startswith="Town House"))
    )

    commuteWeight = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Commute_Range_Max_Scale)],
        label="Commute Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    moveinDate = forms.DateField(
        label="Move in Date",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': "moveInDatePicker",
                'placeholder': 'Choose move in day',
            },
            format='%m/%d/%Y',
    ))

    numBedrooms = forms.ChoiceField(
        choices=[(x, x) for x in range(1, Num_Bedrooms_Max)],
        label="Number of Bedrooms",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )


class InteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields in regards to the interior Admenities
    """
    minBathrooms = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    maxBathrooms = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    airConditioning = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Air conditioning",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    washDryer_InHome = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Wash + Dryer in Home",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    dishWasher = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Dish Washer",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    bath = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Bath",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )


class RentSurvey(RentSurveyBase, InteriorAmenitiesForm):
    """
    Rent Survey is the rent survey on the main survey page
    """
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        exclude = ['userProf', 'survey_type']


class RentSurveyMini(RentSurveyBase, InteriorAmenitiesForm):
    """
    RentSurveyMini is the survey that is on the survey results page and allows the user to create
    quick changes. This should be mostly a subset of the RentSurvey
    """

    class Meta:
        model = RentingSurveyModel
        exclude = ['userProf', 'survey_type']


class BuySurvey(ModelForm):
    class Meta:
        model = BuyingSurveyModel
        fields = ['maxPrice',]

