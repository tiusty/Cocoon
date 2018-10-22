from django.contrib import admin
from .models import ItineraryModel
from .models import TimeModel

# Register your models here.

class TimeInline(admin.StackedInline):
    model = TimeModel
    extra = 0

class ItineraryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Client',
         {'fields': ('client', 'homes')}
         ),
        ('Tour',
         {'fields': ('itinerary', 'tour_duration_seconds')}),
        ('Agent',
         {'fields': ('agent', 'selected_start_time')})
    ]

    inlines = [TimeInline]

class TimeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Time',
         {'fields': ('time', 'itinerary')}),
    ]

admin.site.register(ItineraryModel, ItineraryAdmin)
admin.site.register(TimeModel, TimeAdmin)