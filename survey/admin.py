from django.contrib import admin
from survey.models import RentingSurveyModel, RentingDestinationsModel

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3


class AddressInLine(admin.StackedInline):
    model = RentingDestinationsModel
    extra = 0


class RentingSurveyModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_survey", 'id',)
    # noinspection SpellCheckingInspection
    inlines = [AddressInLine]
    fieldsets = (
        (None, {'fields': ('name_survey', 'user_profile_survey')}),
        ('Survey', {'fields': ('home_type_survey', 'min_price_survey', 'max_price_survey', 'min_commute_survey',
                               'max_commute_survey', 'commute_weight_survey', 'commute_type_survey','min_bathrooms_survey',
                               'max_bathrooms_survey', )}),
        ('Interior Amenities',
         {'fields': ('air_conditioning_survey', 'interior_washer_dryer_survey',)}),
        ('Created', {'fields': ('created_survey', 'id',)}),
    )
    list_display = ('name', 'user_profile_survey', )
    list_filter = ['user_profile_survey']
    search_fields = ('name_survey',)


class RentDestinationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rent Destination',
         {'fields': ['survey_destinations', 'street_address_destination']})
    ]
    list_display = ('survey_destinations',)


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(RentingDestinationsModel, RentDestinationAdmin)
