from django.contrib import admin
from cocoon.survey.models import RentingSurveyModel, RentingDestinationsModel, TenantModel

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3


class AddressInLine(admin.StackedInline):
    model = RentingDestinationsModel


class TenantInLine(admin.TabularInline):
    model = TenantModel
    extra = 0


class RentingSurveyModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", 'id', 'url')
    # noinspection SpellCheckingInspection
    fieldsets = (
        (None, {'fields': ('name', 'user_profile')}),
        ('Survey', {'fields': ('home_type', 'provider', 'desired_price', 'max_price', 'min_bathrooms',
                               'max_bathrooms', )}),
        ('Exterior Amenities', {'fields': ('parking_spot',)}),
        ('Created', {'fields': ('created', 'id', 'url')}),
    )
    list_display = ('name', 'user_profile', )
    list_filter = ['user_profile']
    search_fields = ('name',)
    inlines = [TenantInLine]


class RentDestinationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rent Destination',
         {'fields': ['street_address', 'max_commute', 'min_commute', 'commute_weight', 'commute_type',]})
    ]


class TenantModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tenant',
         {
             'fields': ['first_name', 'last_name', 'is_student', 'survey'],
         })
    ]
    inlines = [AddressInLine]


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(RentingDestinationsModel, RentDestinationAdmin)
admin.site.register(TenantModel, TenantModelAdmin)
