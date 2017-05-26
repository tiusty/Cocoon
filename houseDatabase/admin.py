from django.contrib import admin
from .models import RentDatabase

# Register your models here.

class HouseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['address']}),
        ('House Info', {'fields': ('price', 'home_type', 'numBedrooms', 'moveInDay','numBathrooms','air_conditioning','washDryer_InHome','dishWasher','bath','lon', 'lat',),}),
    ]

    list_display = ('address', 'price', 'home_type', 'numBedrooms', 'moveInDay', 'air_conditioning', 'lon', 'lat',)
    list_filter = ['home_type']
    search_fields = ['address']

admin.site.register(RentDatabase, HouseAdmin)