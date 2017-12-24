from django.contrib import admin
from .models import RentDatabase, ZipCodeDictionary,ZipCodeDictionaryChild, HousePhotos


class HousePhotoUrlInLine(admin.StackedInline):
    model = HousePhotos
    extra = 0


# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('House Info',
         {'fields': ['_street_address_home', '_city_home', '_state_home', '_zip_code_home', '_price_home',
                     '_home_type', '_move_in_day', '_latitude_home', '_longitude_home', ]}),
        ('Interior Amenities',
         {'fields': ('_air_conditioning', '_washer_dryer_in_home', '_dish_washer',
                     '_bath', '_num_bedrooms', '_num_bathrooms',), }),
        ('Exterior Amenities',
         {'fields': ('_parking_spot', '_washer_dryer_in_building', '_elevator',
                     '_handicap_access', '_pool_hot_tub', '_fitness_center', '_storage_unit',), }),
    ]

    list_display = ('street_address', 'price', 'home_type', 'move_in_day', 'num_bedrooms',
                    'latitude', 'longitude',)
    list_filter = ['_home_type']
    search_fields = ['address']
    inlines = [HousePhotoUrlInLine]


class ZipCodeDictionaryChildInLine(admin.StackedInline):
    model = ZipCodeDictionaryChild
    extra = 0


class ZipCodeDictionaryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ZipCodes',
         {'fields': ['zip_code', ]}),
    ]
    list_display = ('zip_code',)
    inlines = [ZipCodeDictionaryChildInLine]


admin.site.register(RentDatabase, HouseAdmin)
admin.site.register(ZipCodeDictionary, ZipCodeDictionaryAdmin)