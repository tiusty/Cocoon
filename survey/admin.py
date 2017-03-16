from django.contrib import admin
from survey.models import RentingSurveyModel, RentingDesintations

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3

class AddressInLine(admin.StackedInline):
    model = RentingDesintations
    extra = 0



class RentingSurveyModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    readonly_fields = ("created",'id',)
    inlines = [ChoiceInline, AddressInLine]
    fieldsets = (
        (None, {'fields': ('name', 'userProf')}),
        ('Survey', {'fields': ('home_type', 'minPrice', 'maxPrice', 'maxCommute', 'minCommute', 'commuteWeight', 'moveinDate',)}),
        ('Created', {'fields': ('created','id',)}),
    )
    list_display = ('name', 'userProf','get_short_name', )
    list_filter = ['userProf']
    search_fields = ('name',)


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)