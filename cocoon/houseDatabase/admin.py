from django.contrib import admin
from .models import RentDatabaseModel, HousePhotos, \
    HomeTypeModel, HomeProviderModel


class HousePhotoUrlInLine(admin.StackedInline):
    model = HousePhotos
    extra = 0


# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('House Info',
         {'fields': ['currently_available', 'last_updated', 'street_address', 'city', 'state', 'zip_code', 'price',
                     'home_type', 'latitude', 'longitude', 'apartment_number','laundromat_nearby', 'date_available',]}),
        ('Exterior Amenities',
         {'fields': ('parking_spot', 'pool', 'patio_balcony', 'gym', 'storage', 'laundry_in_building'), }),
        ('Interior Amenities',
         {'fields': ('furnished', 'hardwood_floors', 'air_conditioning', 'dogs_allowed', 'cats_allowed',
                     'laundry_in_unit', 'dishwasher'), }),
        ('Provider Data',
         {'fields': (
             'listing_provider',
             'listing_agent_id',
             'listing_office_id',
             'listing_number',
             'remarks',
         )}
        ),
    ]

    list_display = ('street_address', 'price', 'home_type', 'currently_available', 'date_available', 'last_updated', 'num_bedrooms',
                    'latitude', 'longitude',)
    list_filter = ['home_type', 'listing_provider',]
    search_fields = ['street_address']
    # noinspection SpellCheckingInspection
    inlines = [HousePhotoUrlInLine]


class HomeTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home Type',
         {'fields': ['home_type', ]})
    ]
    list_display = ('home_type',)


class HomeProviderModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home Type',
         {'fields': ['provider', 'last_updated_feed']})
    ]
    list_display = ('provider',)


admin.site.register(RentDatabaseModel, HouseAdmin)
admin.site.register(HomeTypeModel, HomeTypeModelAdmin)
admin.site.register(HomeProviderModel, HomeProviderModelAdmin)
