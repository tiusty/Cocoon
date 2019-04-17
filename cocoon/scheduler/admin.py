from django.contrib import admin
from .models import ItineraryModel
from .models import TimeModel
from .models import HomeVisitModel

class VisitInline(admin.StackedInline):
    model = HomeVisitModel
    extra = 0


class TimeInline(admin.StackedInline):
    model = TimeModel
    extra = 0


class ItineraryAdmin(admin.ModelAdmin):
    raw_id_fields = ('homes',)
    list_display = ('client', 'agent', 'finished')
    search_fields = ('client__email',)
    list_filter = ['client', 'finished', ]

    inlines = [VisitInline, TimeInline]


class VisitAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home',
         {'fields': ('home', 'travel_time', 'visit_index')}),
    ]


class TimeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Time',
         {'fields': ('time', 'itinerary')}),
    ]


admin.site.register(ItineraryModel, ItineraryAdmin)
admin.site.register(TimeModel, TimeAdmin)
admin.site.register(HomeVisitModel, VisitAdmin)
