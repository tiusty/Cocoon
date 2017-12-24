from django.contrib import admin
from survey.models import RentingSurveyModel, RentingDestinations, HomeType

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3


class AddressInLine(admin.StackedInline):
    model = RentingDestinations
    extra = 0


class RentingSurveyModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    readonly_fields = ("created", 'id',)
    inlines = [AddressInLine]
    fieldsets = (
        (None, {'fields': ('_name', '_user_profile')}),
        ('Survey', {'fields': ('_home_type', '_min_price', '_max_price', '_min_commute',
                               '_max_commute', '_commute_weight', '_min_bathrooms', '_max_bathrooms', )}),
        ('Interior Amenities',
         {'fields': ('_air_conditioning',)}),
        ('Created', {'fields': ('created', 'id',)}),
    )
    list_display = ('name', '_user_profile', )
    list_filter = ['_user_profile']
    search_fields = ('name',)


class HomeTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home Type',
         {'fields': ['homeType', ]})
    ]
    list_display = ('homeType',)


class RentDestinationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Rent Destination',
         {'fields': ['survey', 'street_address']})
    ]
    list_display = ('survey',)


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(HomeType, HomeTypeModelAdmin)
admin.site.register(RentingDestinations, RentDestinationAdmin)
