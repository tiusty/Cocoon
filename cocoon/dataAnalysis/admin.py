from django.contrib import admin
from django.db.models import Avg, Max, Min

from .models import SurveyResultsIteration, HomeTracker
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field


class SurveyResultIterationResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Iteration Id')
    user_email = Field(attribute='user_email', column_name='Users Email')
    survey_id = Field(attribute='survey_id', column_name='Survey Id')
    user_full_name = Field(attribute='user_full_name', column_name='User Full Name')
    avg_home_score = Field(column_name='Avg Home Score')
    standard_deviation_homes = Field(column_name="Standard Deviation Of Homes")
    max_score_home = Field(column_name='Max score for a home')
    min_score_home = Field(column_name='Min Score for a home')
    num_homes = Field(column_name='Number of Homes')

    @staticmethod
    def dehydrate_max_score_home(iteration):
        return iteration.homes.all().aggregate(Max('score'))['score__max']

    @staticmethod
    def dehydrate_min_score_home(iteration):
        return iteration.homes.all().aggregate(Min('score'))['score__min']

    @staticmethod
    def dehydrate_standard_deviation_homes(iteration):
        scores = []
        for home in iteration.homes.all():
            scores.append(home.score)
        avg = iteration.homes.all().aggregate(Avg('score'))['score__avg']

        score_normalized = []
        for score in scores:
            score_normalized.append((score - avg) ** 2)
        variance = 0
        if len(score_normalized) > 0:
            variance = sum(score_normalized)/len(score_normalized)
        return variance ** .5

    @staticmethod
    def dehydrate_avg_home_score(iteration):
        return iteration.homes.all().aggregate(Avg('score'))['score__avg']

    @staticmethod
    def dehydrate_num_homes(iteration):
        return iteration.homes.all().count()

    class Meta:
        model = SurveyResultsIteration
        fields = ('id', 'user_email', 'user_full_name', 'survey_id')


class HomeTrackerInLIne(admin.TabularInline):
    model = HomeTracker
    extra = 0


class SurveyResultsIterationAdmin(ImportExportModelAdmin):
    resource_class = SurveyResultIterationResource
    inlines = [HomeTrackerInLIne]


admin.site.register(SurveyResultsIteration, SurveyResultsIterationAdmin)