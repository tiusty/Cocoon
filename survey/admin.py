from django.contrib import admin
from survey.models import RentingSurveyModel, RentingDestinations, HomeType

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = RentingSurveyModel
    extra = 3


class AddressInLine(admin.StackedInline):
    model = RentingDestinations
    extra = 0


class RentingSurveyModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    readonly_fields = ("created", 'id',)
    inlines = [AddressInLine]
    fieldsets = (
        (None, {'fields': ('name', 'user_profile')}),
        ('Survey', {'fields': ('home_type', 'min_price', 'max_price', 'min_commute',
                               'max_commute', 'commute_weight', 'min_bathrooms', 'max_bathrooms', )}),
        ('Created', {'fields': ('created', 'id',)}),
    )
    list_display = ('name', 'user_profile', 'get_short_name', )
    list_filter = ['user_profile']
    search_fields = ('name',)


class HomeTypeModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Home Type',
         {'fields': ['homeType', ]})
    ]
    list_display = ('homeType',)


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(HomeType, HomeTypeModelAdmin)
