from django.contrib import admin
from .models import ItineraryModel
from .models import TimeModel

# Register your models here.


class TimeInline(admin.StackedInline):
    model = TimeModel
    extra = 0


class ItineraryAdmin(admin.ModelAdmin):
    raw_id_fields = ('homes',)

    inlines = [TimeInline]


class TimeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Time',
         {'fields': ('time', 'itinerary')}),
    ]


admin.site.register(ItineraryModel, ItineraryAdmin)
admin.site.register(TimeModel, TimeAdmin)