# Django modules
from django import forms
from django.forms import ModelForm

# Survey models
from cocoon.survey.models import RentingSurveyModel, HomeInformationModel, CommuteInformationModel, \
    PriceInformationModel, InteriorAmenitiesModel, ExteriorAmenitiesModel, HouseNearbyAmenitiesModel, \
    DestinationsModel, TenantModel, TenantPersonalInformationModel
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType

# Python global configurations
from config.settings.Global_Config import MAX_TEXT_INPUT_LENGTH, MAX_NUM_BEDROOMS
from .constants import WEIGHT_QUESTION_MAX, MOVE_WEIGHT_MAX, HYBRID_WEIGHT_MAX
from django.forms.models import inlineformset_factory

# import constants
from cocoon.survey.constants import MAX_TENANTS_FOR_ONE_SURVEY


class HomeInformationForm(ModelForm):
    num_bedrooms = forms.IntegerField(
        required=False,
        max_value=MAX_NUM_BEDROOMS,
        min_value=0,
    )

    home_type = forms.ModelMultipleChoiceField(
        required=True,
        queryset=HomeTypeModel.objects.all()
    )

    polygon_filter_type = forms.IntegerField(
        required=False,
        max_value=1,
        min_value=0,
    )

    move_weight = forms.IntegerField(
        required=False,
        max_value=MOVE_WEIGHT_MAX,
        min_value=0
    )

    earliest_move_in = forms.DateTimeField(
        required=False,
    )

    latest_move_in = forms.DateTimeField(
        required=False
    )

    def is_valid(self):
        valid = super().is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        if 'move_weight' in current_form:

            # only when the commute type is not work from home are these fields needed
            if current_form['move_weight'] != MOVE_WEIGHT_MAX:

                if current_form['earliest_move_in'] is None:
                    self.add_error('earliest_move_in', "If move weight is not Move asap, earliest move in required")
                    valid = False

                if current_form['latest_move_in'] is None:
                    self.add_error('latest_move_in', "If move weight is not Move asap, latest move in required")
                    valid = False

        return valid

    class Meta:
        model = HomeInformationModel
        fields = ('num_bedrooms', 'home_type', 'polygon_filter_type', 'move_weight', 'earliest_move_in',
                  'latest_move_in')


class PriceInformationForm(ModelForm):

    max_price = forms.IntegerField(
        required=True
    )

    desired_price = forms.IntegerField(
        required=True
    )

    price_weight = forms.IntegerField(
        required=True,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    class Meta:
        model = PriceInformationModel
        fields = ('max_price', 'desired_price', 'price_weight')


class HouseNearbyAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the HouseNearbyAmenitiesModel Model
    """

    wants_laundry_nearby = forms.BooleanField(
        required=False,
    )

    laundry_nearby_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    class Meta:
        model = HouseNearbyAmenitiesModel
        fields = ('wants_laundry_nearby', 'laundry_nearby_weight')


class ExteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the ExteriorAmenitiesModel Model
    """
    wants_parking = forms.BooleanField(
        required=False,
    )

    wants_laundry_in_building = forms.BooleanField(
        required=False,
    )

    laundry_in_building_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    number_of_cars = forms.IntegerField(
        required=False,
        min_value=0,
    )

    wants_patio = forms.BooleanField(
        required=False,
    )

    patio_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_pool = forms.BooleanField(
        required=False,
    )

    pool_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_gym = forms.BooleanField(
        required=False,
    )

    gym_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_storage = forms.BooleanField(
        required=False,
    )

    storage_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    class Meta:
        model = ExteriorAmenitiesModel
        fields = ('wants_parking', 'wants_laundry_in_building', 'laundry_in_building_weight', 'number_of_cars',
                  'wants_patio', 'patio_weight', 'wants_pool', 'pool_weight', 'wants_gym', 'gym_weight',
                  'wants_storage', 'storage_weight',)


class InteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the BuildingExteriorAmenitiesModel Model
    """
    wants_laundry_in_unit = forms.BooleanField(
        required=False,
    )

    laundry_in_unit_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_furnished = forms.BooleanField(
        required=False,
    )

    furnished_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_dogs = forms.BooleanField(
        required=False,
    )

    service_dogs = forms.BooleanField(
        required=False,
    )

    dog_size = forms.CharField(
        required=False,
    )

    breed_of_dogs = forms.CharField(
        required=False,
    )

    number_of_dogs = forms.IntegerField(
        required=False,
        min_value=0,
    )

    wants_cats = forms.BooleanField(
        required=False,
    )

    cat_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_hardwood_floors = forms.BooleanField(
        required=False,
    )

    hardwood_floors_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_AC = forms.BooleanField(
        required=False,
    )

    AC_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    wants_dishwasher = forms.BooleanField(
        required=False,
    )

    dishwasher_weight = forms.IntegerField(
        required=False,
        max_value=WEIGHT_QUESTION_MAX,
        min_value=0,
    )

    class Meta:
        model = InteriorAmenitiesModel
        fields = ('wants_laundry_in_unit', 'laundry_in_unit_weight', 'wants_furnished', 'furnished_weight',
                  'wants_dogs', 'service_dogs', 'dog_size', 'breed_of_dogs', 'number_of_dogs', 'wants_cats',
                  'cat_weight', 'wants_hardwood_floors', 'hardwood_floors_weight', 'wants_AC', 'AC_weight',
                  'wants_dishwasher', 'dishwasher_weight')


class RentSurveyForm(InteriorAmenitiesForm, ExteriorAmenitiesForm, HouseNearbyAmenitiesForm, PriceInformationForm,
                     HomeInformationForm):
    """
    Rent Survey is the rent survey on the main survey page
    """
    number_of_tenants = forms.IntegerField(
        required=True,
        max_value=MAX_TENANTS_FOR_ONE_SURVEY,
        min_value=1,
    )

    class Meta:
        model = RentingSurveyModel
        fields = InteriorAmenitiesForm.Meta.fields + ExteriorAmenitiesForm.Meta.fields + \
            HouseNearbyAmenitiesForm.Meta.fields + PriceInformationForm.Meta.fields + \
            HomeInformationForm.Meta.fields + ('number_of_tenants',)


class RentSurveyFormEdit(InteriorAmenitiesForm, ExteriorAmenitiesForm, HouseNearbyAmenitiesForm, PriceInformationForm,
                         HomeInformationForm):
    """
    Same as above but the user cannot change how many tenants there are
    """

    class Meta:
        model = RentingSurveyModel
        fields = InteriorAmenitiesForm.Meta.fields + ExteriorAmenitiesForm.Meta.fields + \
            HouseNearbyAmenitiesForm.Meta.fields + PriceInformationForm.Meta.fields + \
            HomeInformationForm.Meta.fields


class DestinationForm(ModelForm):
    street_address = forms.CharField(
        required=False,
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    city = forms.CharField(
        required=False,
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    state = forms.CharField(
        required=False,
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    zip_code = forms.CharField(
        required=False,
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    class Meta:
        model = DestinationsModel
        fields = ('street_address', 'city', 'state', 'zip_code')


class CommuteInformationForm(DestinationForm):

    max_commute = forms.IntegerField(
        required=False,
    )

    desired_commute = forms.IntegerField(
        required=False,
    )

    commute_weight = forms.IntegerField(
        required=False,
    )

    commute_type = forms.ModelChoiceField(
        required=True,
        queryset=CommuteType.objects.all(),
    )

    traffic_option = forms.BooleanField(
        required=False,
    )

    def is_valid(self):
        valid = super().is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        if 'commute_type' in current_form:

            # only when the commute type is not work from home are these fields needed
            if current_form['commute_type'] != CommuteType.objects.get_or_create(commute_type=CommuteType.WORK_FROM_HOME)[0]:

                if not current_form['street_address']:
                    self.add_error('street_address', "Street Address Required")
                    valid = False

                if not current_form['city']:
                    self.add_error('city', "City Required")
                    valid = False

                if not current_form['state']:
                    self.add_error('state', "State required")
                    valid = False

                if not current_form['zip_code']:
                    self.add_error('zip_code', "Zip Code Required")
                    valid = False

                if not current_form['commute_weight']:
                    self.add_error('commute_weight', "Commute weight needed")
                    valid = False

                if current_form['max_commute'] is not None:
                    if int(current_form['max_commute']) < 0:
                        self.add_error('max_commute', "Max Commute needs to be above 0")
                        valid = False
                else:
                    self.add_error('max_commute', "Max Commute Needed")
                    valid = False

                if current_form['desired_commute'] is not None:
                    if int(current_form['desired_commute']) < 0:
                        self.add_error('desired_commute', "Min commute needs to be above 0")
                        valid = False

                if current_form['desired_commute'] is not None and current_form['max_commute'] is not None:
                    if int(current_form['desired_commute']) > int(current_form['max_commute']):
                        self.add_error('max_commute', "Max commute needs to be above min commute")
                        valid = False

        return valid

    class Meta:
        model = CommuteInformationModel
        fields = DestinationForm.Meta.fields + ('max_commute', 'desired_commute', 'commute_weight', 'commute_type',
                                                'traffic_option')


class TenantPersonalInformationForm(ModelForm):
    first_name = forms.CharField(
        required=True
    )

    last_name = forms.CharField(
        required=True
    )

    occupation = forms.CharField(
        required=False,
    )

    other_occupation_reason = forms.CharField(
        required=False,
    )

    unemployed_follow_up = forms.CharField(
        required=False,
    )

    income = forms.CharField(
        required=False,
    )

    credit_score = forms.CharField(
        required=False,
    )

    new_job = forms.CharField(
        required=False,
    )

    class Meta:
        model = TenantPersonalInformationModel
        fields = ('first_name', 'last_name', 'occupation', 'other_occupation_reason', 'unemployed_follow_up',
                  'income', 'credit_score', 'new_job')


class TenantForm(CommuteInformationForm, TenantPersonalInformationForm):
    class Meta:
        model = TenantModel
        fields = CommuteInformationForm.Meta.fields + TenantPersonalInformationForm.Meta.fields


class TenantFormJustNames(TenantPersonalInformationForm):
    class Meta:
        model = TenantModel
        fields = ('first_name', 'last_name')


TenantFormSet = inlineformset_factory(RentingSurveyModel, TenantModel, form=TenantForm,
                                      extra=4, can_delete=False)
TenantFormSetJustNames = inlineformset_factory(RentingSurveyModel, TenantModel, form=TenantFormJustNames,
                                               extra=0, can_delete=False)
