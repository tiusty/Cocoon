from django.contrib import admin
from survey.models import RentingSurveyModel

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3


class RentingSurveyModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('get_short_name', )
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)