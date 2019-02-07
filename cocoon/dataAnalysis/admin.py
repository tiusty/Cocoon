from django.contrib import admin

from .models import SurveyResultsIteration, HomeTracker


class HomeTrackerInLIne(admin.TabularInline):
    model = HomeTracker
    extra = 0


class SurveyResultsIterationAdmin(admin.ModelAdmin):
    inlines = [HomeTrackerInLIne]


admin.site.register(SurveyResultsIteration, SurveyResultsIterationAdmin)