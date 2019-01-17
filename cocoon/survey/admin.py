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
    readonly_fields = ("created", 'id', 'url')
    raw_id_fields = ("favorites", "visit_list",)
    # noinspection SpellCheckingInspection
    fieldsets = (
        (None, {'fields': ('name', 'user_profile')}),
        ('Survey', {'fields': ('home_type', 'desired_price', 'max_price', 'min_bathrooms',
                               'max_bathrooms', )}),
        ('Exterior Amenities', {'fields': ('parking_spot',)}),
        ('Created', {'fields': ('created', 'id', 'url')}),
        ('Homes', {'fields': ('favorites', 'visit_list', 'polygon_filter_type',)}),
    )
    list_display = ('name', 'user_profile', )
    list_filter = ['user_profile']
    search_fields = ('name',)
    inlines = [TenantInLine, PolygonInLine]


class TenantModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tenant',
         {
             'fields': ['first_name', 'last_name', 'is_student', 'survey'],
         }),
        ('Rent Destination',
         {'fields': ['street_address', 'max_commute', 'min_commute', 'commute_weight', 'commute_type',]})
    ]


class PolygonModelAdmin(admin.ModelAdmin):
    inlines = [VertexInLine]


admin.site.register(RentingSurveyModel, RentingSurveyModelAdmin)
admin.site.register(PolygonModel, PolygonModelAdmin)
admin.site.register(TenantModel, TenantModelAdmin)
