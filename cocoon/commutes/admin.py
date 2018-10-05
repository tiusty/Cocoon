# Django Imports
from django.contrib import admin

# Commute imports
from .models import ZipCodeBase, ZipCodeChild, CommuteType, TransitType


class ZipCodeChildInLine(admin.StackedInline):
    model = ZipCodeChild
    extra = 0


class ZipCodeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ZipCodes',
         {'fields': ['zip_code', ]}),
    ]
    list_display = ('zip_code',)
    search_fields = ['zip_code']
    # noinspection SpellCheckingInspection
    inlines = [ZipCodeChildInLine]


class CommuteTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Commute Type',
         {'fields': ['commute_type', ]})
    ]
    list_display = ('commute_type',)

class TransitTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Transit Type',
         {'fields': ['transit_type', ]})
    ]
    list_display = ('transit_type',)

admin.site.register(ZipCodeBase, ZipCodeAdmin)
admin.site.register(CommuteType, CommuteTypeAdmin)
admin.site.register(TransitType, TransitTypeAdmin)