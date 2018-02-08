from django.contrib import admin
from .models import RentDatabaseModel, ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel, HousePhotosModel, \
    HomeTypeModel, CommuteTypeModel, DatabaseManagementModel


class HousePhotoUrlInLine(admin.StackedInline):
    model = HousePhotosModel
    extra = 0


# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('House Info',
         {'fields': ['currently_available_home', 'last_updated_home', 'street_address_home', 'city_home', 'state_home', 'zip_code_home', 'price_home',
                     'home_type_home', 'latitude_home', 'longitude_home', ]}),
        ('Interior Amenities',
         {'fields': ('air_conditioning_home', 'interior_washer_dryer_home', 'dish_washer_home',
                     'bath_home', 'num_bedrooms_home', 'num_bathrooms_home',), }),
        ('Exterior Amenities',
         {'fields': ('parking_spot_home', 'building_washer_dryer_home', 'elevator_home',
                     'handicap_access_home', 'pool_hot_tub_home', 'fitness_center_home', 'storage_unit_home',), }),
        ('MLS Pin Data',
         {'fields': (
             'listing_provider_home',
             'listing_agent_home',
             'listing_office_home'
         )}
        )
    ]

    list_display = ('street_address_home', 'price_home', 'home_type_home', 'currently_available_home', 'last_updated_home', 'num_bedrooms_home',
                    'latitude_home', 'longitude_home',)
    list_filter = ['home_type_home']
    search_fields = ['street_address_home']
    # noinspection SpellCheckingInspection
    inlines = [HousePhotoUrlInLine]

class ZipCodeDictionaryChildInLine(admin.StackedInline):
    model = ZipCodeDictionaryChildModel
    extra = 0
    
class DatabaseManagementModelAdmin(admin.ModelAdmin):
    pass

class ZipCodeDictionaryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ZipCodes',
         {'fields': ['zip_code_parent', ]}),
    ]
    list_display = ('zip_code_parent',)
    # noinspection SpellCheckingInspection
    inlines = [ZipCodeDictionaryChildInLine]


class HomeTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home Type',
         {'fields': ['home_type_survey', ]})
    ]
    list_display = ('home_type_survey',)


class CommuteTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Commute Type',
         {'fields': ['commute_type_field',]})
    ]
    list_display = ('commute_type_field',)


admin.site.register(RentDatabaseModel, HouseAdmin)
admin.site.register(ZipCodeDictionaryParentModel, ZipCodeDictionaryAdmin)
admin.site.register(HomeTypeModel, HomeTypeModelAdmin)
admin.site.register(CommuteTypeModel, CommuteTypeModelAdmin)
admin.site.register(DatabaseManagementModel, DatabaseManagementModelAdmin)
