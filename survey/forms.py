from django import forms
from survey.models import RentingSurveyModel, BuyingSurveyModel, RentingDesintations, HomeType
from django.forms import ModelForm
from django.db.models import Q



class DestinationForm(ModelForm):
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

    class Meta:
        model = RentingDesintations
        fields = ['streetAddress', 'city', 'state', 'zip_code']


class RentSurvey(ModelForm):
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

    home_type=forms.ModelMultipleChoiceField(
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
    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        fields = ['home_type', 'maxPrice', 'minPrice']


class RentSurveyMini(ModelForm):
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
    name = forms.CharField(
        label="Survey Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of the survey',
            }),
        max_length=200,
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
    class Meta:
        model = RentingSurveyModel
        fields = ['home_type', 'maxPrice', 'minPrice', 'name']


class BuySurvey(ModelForm):
    class Meta:
        model = BuyingSurveyModel
        fields = ['maxPrice',]

