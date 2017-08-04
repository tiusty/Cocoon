from django.contrib import admin
from .models import RentDatabase, ZipCodeDictionary,ZipCodeDictionaryChild, HousePhotos


class HousePhotoUrlInLine(admin.StackedInline):
    model = HousePhotos
    extra = 0


# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('House Info',
         {'fields': ['address', 'city', 'state', 'zip_code', 'price',
                     'home_type', 'move_in_day', 'lat', 'lon', ]}),
        ('Interior Amenities',
         {'fields': ('air_conditioning', 'wash_dryer_in_home', 'dish_washer',
                     'bath', 'num_bedrooms', 'num_bathrooms',), }),
        ('Exterior Amenities',
         {'fields': ('parking_spot', 'washer_dryer_in_building', 'elevator',
                     'handicap_access', 'pool_hot_tub', 'fitness_center', 'storage_unit',), }),
    ]

    list_display = ('address', 'price', 'home_type', 'move_in_day', 'num_bedrooms',
                    'lat', 'lon',)
    list_filter = ['home_type']
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