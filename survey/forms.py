from django import forms
from survey.models import RentingSurveyModel, BuyingSurveyModel, RentingDesintations, HomeType, default_rent_survey_name
from django.forms import ModelForm
from django.db.models import Q

import datetime

# Python global configurations
from Unicorn.settings.Global_Config import \
    Max_Num_Bathrooms, Max_Text_Input_Length, \
    Max_Num_Bedrooms, Hybrid_weighted_max


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
    # if name is left blank it sets a default name
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

    price_weight = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Price Weight",
        widget=forms.Select(
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
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Commute Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    moveinDateStart = forms.DateField(
        label="Start of move in range",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': "moveInDatePickerStart",
                'placeholder': 'Choose first day to move in',
            },
            format='%m/%d/%Y',
        ))


    moveinDateEnd = forms.DateField(
        label="End of move in range",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'id': "moveInDatePickerEnd",
                'placeholder': 'Choose last date to move in',
            },
            format='%m/%d/%Y',
        ))

    numBedrooms = forms.ChoiceField(
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
        if current_form['moveinDateStart'] < datetime.date.today():
            self.add_error('moveinDateStart', "Start Day should not be in the past")
            valid = False

        # Makes sure that the End day is after the start day
        if current_form['moveinDateStart'] > current_form['moveinDateEnd']:
            self.add_error('moveinDateEnd', "End date should not be before the start date")
            valid = False

        # Make sure that the minimum number of bathrooms is not less then 0
        if current_form['minBathrooms'] < 0:
            self.add_error('minBathrooms', "You can't have less than 0 bathrooms")
            valid = False

        # make sure that the max number of bathrooms is not greater than the max specified
        if current_form['maxBathrooms'] > Max_Num_Bathrooms:
            self.add_error('maxBathrooms', "You can't have more bathrooms than " + str(Max_Num_Bathrooms))
            valid = False

        # Make sure the bedrooms is at least 1
        # With the choice fields, the field needs to be casted as an int since it
        # Is stored as a string in cleaned_data
        if int(current_form['numBedrooms']) < 1:
            self.add_error('numBedrooms', "There can't be less than 1 bedroom")
            valid = False

        # Make sure the bedrooms are not more than the max allowed
        if int(current_form['numBedrooms']) > Max_Num_Bedrooms:
            self.add_error('numBedrooms', "There can't be more than " + str(Max_Num_Bedrooms))
            valid = False

        # Make sure
        if int(current_form['commuteWeight']) > Hybrid_weighted_max:
            self.add_error('commuteWeight', "Commute weight cant' be greater than " + str(Hybrid_weighted_max))
            valid = False

        if int(current_form['commuteWeight']) < 0:
            self.add_error('commuteWeight', "Commute weight cant' be less than 0")
            valid = False

        return valid


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


class BuildingExteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the BuildingExteriorAmenities Model
    """
    parkingSpot = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Parking Spot",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    washerDryer_inBuilding = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Washer/Dryer in Building",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    elevator = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Elevator",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    handicapAccess = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Handicap Access",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    poolHottub = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Pool/Hot tub",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    fitnessCenter = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
        label="Fitness Center",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    storageUnit = forms.ChoiceField(
        choices=[(x, x) for x in range(0, Hybrid_weighted_max)],
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
        exclude = ['userProf', 'survey_type', 'name',]


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
        exclude = ['userProf', 'survey_type']


class BuySurvey(ModelForm):
    class Meta:
        model = BuyingSurveyModel
        fields = ['maxPrice', ]
