from django.contrib import admin
from .models import ItineraryModel

# Register your models here.


class ItineraryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Client',
         {'fields': ('client', 'homes')}
         ),
        ('Tour',
         {'fields': ('itinerary', 'tour_duration_seconds', 'available_start_times')}),
        ('Agent',
         {'fields': ('agent', 'selected_start_time')})
    ]


admin.site.register(ItineraryModel, ItineraryAdmin)
