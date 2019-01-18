from django.contrib import admin
from cocoon.survey.models import RentingSurveyModel, TenantModel

# Register your models here.


class TenantInLine(admin.TabularInline):
    model = TenantModel
    extra = 0


class RentingSurveyModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", 'id', 'url')
    raw_id_fields = ("favorites", "visit_list",)
    # noinspection SpellCheckingInspection
    fieldsets = (
        (None, {'fields': ('name', 'user_profile')}),
        ('Survey', {'fields': ('home_type', 'desired_price', 'max_price', 'min_bathrooms',
                               'max_bathrooms',)}),
        ('Nearby Amenities', {'fields': ('wants_laundry_nearby',)}),
        ('Exterior Amenities', {'fields': ('wants_parking', 'wants_laundry_in_building', 'wants_patio',
                                           'patio_weight', 'wants_pool', 'pool_weight', 'wants_gym', 'gym_weight',
                                           'wants_storage', 'storage_weight',)}),
        ('Interior Amenities', {'fields': (
            'wants_laundry_in_unit', 'wants_furnished', 'furnished_weight', 'wants_dogs', 'number_of_dogs',
            'service_dogs', 'dog_size', 'breed_of_dogs', 'wants_cats', 'cat_weight',
            'wants_hardwood_floors', 'hardwood_floors_weight', 'wants_AC', 'AC_weight', 'wants_dishwasher',
            'dishwasher_weight',)}),

        ('Created', {'fields': ('created', 'id', 'url')}),
        ('Homes', {'fields': ('favorites', 'visit_list',)}),
    )
    list_display = ('name', 'user_profile',)
    list_filter = ['user_profile']
    search_fields = ('name',)
    inlines = [TenantInLine]


class TenantModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tenant',
         {
             'fields': ['first_name', 'last_name', 'is_student', 'survey'],
         }),
        ('Rent Destination',
         {'fields': ['street_address', 'max_commute', 'min_commute', 'commute_weight', 'commute_type',]})
    ]


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(TenantModel, TenantModelAdmin)
