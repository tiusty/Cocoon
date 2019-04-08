from django.contrib import admin
from cocoon.survey.models import RentingSurveyModel, TenantModel, PolygonModel, VertexModel

# Register your models here.


class TenantInLine(admin.TabularInline):
    model = TenantModel
    extra = 0


class VertexInLine(admin.TabularInline):
    model = VertexModel
    extra = 0


class PolygonInLine(admin.TabularInline):
    model = PolygonModel
    inlines = [VertexInLine]
    extra = 0


class RentingSurveyModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", 'id', 'url', 'survey_name', 'num_bedrooms')
    raw_id_fields = ("favorites", "visit_list", "blacklisted_homes")
    # noinspection SpellCheckingInspection
    fieldsets = (
        (None, {'fields': ('survey_name', 'user_profile')}),
        ('Survey', {'fields': ('home_type', 'desired_price', 'max_price', 'price_weight', 'min_bathrooms',
                               'max_bathrooms', 'move_weight', 'num_bedrooms', 'earliest_move_in', 'latest_move_in',)}),
        ('Nearby Amenities', {'fields': ('wants_laundry_nearby', 'laundry_nearby_weight',)}),
        ('Exterior Amenities', {'fields': ('wants_parking', 'wants_laundry_in_building', 'laundry_in_building_weight',
                                           'wants_patio',
                                           'patio_weight', 'wants_pool', 'pool_weight', 'wants_gym', 'gym_weight',
                                           'wants_storage', 'storage_weight',)}),
        ('Interior Amenities', {'fields': (
            'wants_laundry_in_unit', 'laundry_in_unit_weight', 'wants_furnished', 'furnished_weight', 'wants_dogs', 'number_of_dogs', 'dog_weight',
            'service_dogs', 'dog_size', 'breed_of_dogs', 'wants_cats', 'cat_weight',
            'wants_hardwood_floors', 'hardwood_floors_weight', 'wants_AC', 'AC_weight', 'wants_dishwasher',
            'dishwasher_weight',)}),

        ('Created', {'fields': ('created', 'id', 'url')}),
        ('Homes', {'fields': ('favorites', 'visit_list', 'polygon_filter_type',)}),
        ('Update Info', {'fields': ('last_updated', 'update_frequency', 'wants_update', 'score_threshold', 'num_home_threshold', 'blacklisted_homes')})
    )
    list_display = ('survey_name', 'user_profile',)
    search_fields = ('user_profile__user__email', 'user_profile__user__first_name', 'user_profile__user__last_name')
    inlines = [TenantInLine, PolygonInLine]


class TenantModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tenant',
         {
             'fields': ['first_name', 'last_name', 'is_student', 'survey'],
         }),
        ('Rent Destination',
         {'fields': ['street_address', 'max_commute', 'desired_commute', 'commute_weight', 'commute_type',]})
    ]


class PolygonModelAdmin(admin.ModelAdmin):
    inlines = [VertexInLine]


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(PolygonModel, PolygonModelAdmin)
admin.site.register(TenantModel, TenantModelAdmin)
