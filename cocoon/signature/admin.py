from django.contrib import admin

# Register your models here.

from cocoon.signature.models import HunterDocTemplateModel, HunterDocModel, HunterDocManagerModel


class HunterDocTemplateModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('template_type', 'template_id')}),
    )


class HunterDocModelInLine(admin.StackedInline):
    model = HunterDocModel
    extra = 0


class HunterDocManagerModelAdmin(admin.ModelAdmin):
    search_fields = ('user__email',)
    list_display = ('user', '__str__',)
    fieldsets = (
        (None, {'fields': ('user',)}),
    )
    inlines = [HunterDocModelInLine]


admin.site.register(HunterDocTemplateModel, HunterDocTemplateModelAdmin)
admin.site.register(HunterDocManagerModel, HunterDocManagerModelAdmin)
