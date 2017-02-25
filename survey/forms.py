from django import forms
from survey.models import RentingSurveyModel, BuyingSurveyModel, RentingDesintations, HomeType, default_rent_survey_name
from django.forms import ModelForm
from django.db.models import Q

# Python global configurations
Commute_Range_Max_Scale = 6 # Remember base 0, so value of 6 is 0-5
Max_Text_Input_Length = 200



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
        choices=[(x,x) for x in range(0,Commute_Range_Max_Scale)],
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
               'id': "moveInDatePicker",
            },
            format='%m/%d/%y',
    ))


class RentSurvey(RentSurveyBase):
    """
    Rent Survey is the rent survey on the main survey page
    """
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        fields = ['name', 'moveinDate', 'home_type', 'maxPrice', 'minPrice', 'commuteWeight', 'maxCommute', 'minCommute']


class RentSurveyMini(RentSurveyBase):
    """
    RentSurveyMini is the survey that is on the survey results page and allows the user to create
    quick changes. This should be mostly a subset of the RentSurvey
    """


    class Meta:
        model = RentingSurveyModel
        fields = ['name', 'moveinDate', 'home_type', 'maxPrice', 'minPrice', 'commuteWeight',
                  'minCommute', 'maxCommute']


class BuySurvey(ModelForm):
    class Meta:
        model = BuyingSurveyModel
        fields = ['maxPrice',]

