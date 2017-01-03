from django import forms
from survey.models import RentingSurveyModel, BuyingSurveyModel
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
    minPrice = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Zip Code',
            }),
    )

    maxPrice = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Zip Code',
            }),
    )

    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        fields = ['streetAddress', 'city', 'state', 'zip_code', 'home_type', 'maxPrice',
                  'minPrice']


class BuySurvey(InitialSurvey):
    class Meta:
        model = BuyingSurveyModel
        fields = ['streetAddress', 'city', 'state', 'zip_code']