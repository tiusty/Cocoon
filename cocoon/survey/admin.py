from django.contrib import admin
from cocoon.survey.models import RentingSurveyModel, RentingDestinationsModel

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3


class AddressInLine(admin.StackedInline):
    model = RentingDestinationsModel
    extra = 0


class RentingSurveyModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_survey", 'id', 'slug')
    # noinspection SpellCheckingInspection
    inlines = [AddressInLine]
    fieldsets = (
        (None, {'fields': ('name_survey', 'user_profile_survey')}),
        ('Survey', {'fields': ('home_type_survey', 'desired_price_survey', 'max_price_survey', 'min_bathrooms_survey',
                               'max_bathrooms_survey', )}),
        ('Interior Amenities',
         {'fields': ('air_conditioning_survey', 'interior_washer_dryer_survey',)}),
        ('Created', {'fields': ('created_survey', 'id', 'slug')}),
    )
    list_display = ('name', 'user_profile_survey', )
    list_filter = ['user_profile_survey']
    search_fields = ('name_survey',)


class RentDestinationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rent Destination',
         {'fields': ['survey', 'street_address', 'max_commute', 'min_commute', 'commute_weight', 'commute_type',]})
    ]
    list_display = ('survey',)


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(RentingDestinationsModel, RentDestinationAdmin)
