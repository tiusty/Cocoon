# Django Imports
from django.contrib import admin

# zip-code imports
from commutes.models import ZipCodeDictionaryParentModel, ZipCodeDictionaryChildModel, CommuteTypeModel


class ZipCodeDictionaryChildInLine(admin.StackedInline):
    model = ZipCodeDictionaryChildModel
    extra = 0


class ZipCodeDictionaryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('ZipCodes',
         {'fields': ['zip_code_parent', ]}),
    ]
    list_display = ('zip_code_parent',)
    search_fields = ['zip_code_parent']
    # noinspection SpellCheckingInspection
    inlines = [ZipCodeDictionaryChildInLine]


class CommuteTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Commute Type',
         {'fields': ['commute_type_field',]})
    ]
    list_display = ('commute_type_field',)


admin.site.register(ZipCodeDictionaryParentModel, ZipCodeDictionaryAdmin)
admin.site.register(CommuteTypeModel, CommuteTypeModelAdmin)