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
         {'fields': ['currently_available', 'last_updated', 'street_address', 'city', 'state', 'zip_code', 'price',
                     'home_type', 'latitude', 'longitude', 'apartment_number', ]}),
        ('Exterior Amenities',
         {'fields': ('parking_spot',), }),
        ('Provider Data',
         {'fields': (
             'listing_provider',
             'listing_agent',
             'listing_office',
             'listing_number'
         )}
        )
    ]

    list_display = ('street_address', 'price', 'home_type', 'currently_available', 'last_updated', 'num_bedrooms',
                    'latitude', 'longitude',)
    list_filter = ['home_type', 'listing_provider',]
    search_fields = ['street_address']
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
