from django.contrib import admin
from .models import RentDatabaseModel, HousePhotos, \
    HomeTypeModel, MlsManagementModel, YglManagementModel, HomeProviderModel


class HousePhotoUrlInLine(admin.StackedInline):
    model = HousePhotos
    extra = 0


# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('House Info',
         {'fields': ['currently_available_home', 'last_updated_home', 'street_address_home', 'city_home', 'state_home', 'zip_code_home', 'price_home',
                     'home_type_home', 'latitude_home', 'longitude_home', 'apartment_number_home', ]}),
        ('Interior Amenities',
         {'fields': ('air_conditioning_home', 'interior_washer_dryer_home', 'dish_washer_home',
                     'bath_home', 'num_bedrooms_home', 'num_bathrooms_home',), }),
        ('Exterior Amenities',
         {'fields': ('parking_spot_home', 'building_washer_dryer_home', 'elevator_home',
                     'handicap_access_home', 'pool_hot_tub_home', 'fitness_center_home', 'storage_unit_home',), }),
        ('Provider Data',
         {'fields': (
             'listing_provider_home',
             'listing_agent_home',
             'listing_office_home',
             'listing_number_home'
         )}
        )
    ]

    list_display = ('street_address_home', 'price_home', 'home_type_home', 'currently_available_home', 'last_updated_home', 'num_bedrooms_home',
                    'latitude_home', 'longitude_home',)
    list_filter = ['home_type_home', 'listing_provider_home',]
    search_fields = ['street_address_home']
    # noinspection SpellCheckingInspection
    inlines = [HousePhotoUrlInLine]


class MlsManagementModelAdmin(admin.ModelAdmin):
    pass


class YglManagementModelAdmin(admin.ModelAdmin):
    pass


class HomeTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home Type',
         {'fields': ['home_type', ]})
    ]
    list_display = ('home_type',)


class HomeProviderModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home Type',
         {'fields': ['provider', ]})
    ]
    list_display = ('provider',)


admin.site.register(RentDatabaseModel, HouseAdmin)
admin.site.register(HomeTypeModel, HomeTypeModelAdmin)
admin.site.register(MlsManagementModel, MlsManagementModelAdmin)
admin.site.register(YglManagementModel, YglManagementModelAdmin)
admin.site.register(HomeProviderModel, HomeProviderModelAdmin)
