from django import forms
from survey.models import RentingSurveyModel
from django.forms import ModelForm


class InitialSurvey(ModelForm):
    streetAddress = forms.CharField(
        label="Destination",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter in a Destination',
                'autocomplete': 'off',
            }),
        max_length=200,
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the city',
            }),
        max_length=200,
    )

    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the State',
            }),
        max_length=200,
    )

    zip_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Zip Code',
            }),
        max_length=200,
    )


class RentSurvey(InitialSurvey):
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        fields = ['streetAddress', 'city', 'state', 'zip_code', 'home_type', 'amountMaxCommuteHigh', 'amountMaxCommuteLow']


class BuySurvey(InitialSurvey):
    name = forms.CharField(max_length=200)