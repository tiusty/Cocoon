from django.contrib import admin
from .models import RentDatabase

# Register your models here.
class HouseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['address']}),
        ('House Info', {'fields': ('price', 'home_type', 'num_bedrooms', 'move_in_day','num_bathrooms','air_conditioning','wash_dryer_in_home','dish_washer','bath','lon', 'lat',),}),
    ]

    list_display = ('address', 'price', 'home_type', 'move_in_day', 'num_bedrooms', 'lon', 'lat',)
    list_filter = ['home_type']
    search_fields = ['address']

admin.site.register(RentDatabase, HouseAdmin)