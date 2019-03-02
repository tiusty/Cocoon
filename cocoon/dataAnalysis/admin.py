# Import Django Modules
from django.contrib import admin

# Import app modules
from .models import SurveyResultsIteration

# Import Third Party Modules
from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field


class SurveyResultIterationResource(resources.ModelResource):
    id = Field(attribute='id', column_name='Iteration Id')
    user_email = Field(attribute='user_email', column_name='Users Email')
    survey_id = Field(attribute='survey_id', column_name='Survey Id')
    user_full_name = Field(attribute='user_full_name', column_name='User Full Name')
    avg_home_score = Field(attribute='avg_home_score', column_name='Avg Home Score')
    avg_home_score_returned = Field(attribute='avg_home_score_returned',column_name='Avg Home Score Returned to User')
    standard_deviation_homes = Field(attribute='standard_deviation_homes', column_name="Standard Deviation Of Homes")
    standard_deviation_homes_returned = Field(attribute='standard_deviation_homes_returned', column_name='Standard Deviation of returned homes')
    max_score_home = Field(attribute='max_score_home', column_name='Max score for a home')
    max_score_home_returned = Field(attribute='max_score_home_returned', column_name='Max Score returned to user')
    min_score_home = Field(attribute='min_score_home', column_name='Min Score for a home')
    min_score_home_returned = Field(attribute='min_score_home_returned', column_name='Min Score returned to user')
    num_homes = Field(attribute='num_homes', column_name='Number of Homes')

    class Meta:
        model = SurveyResultsIteration
        fields = ('id', 'user_email', 'user_full_name', 'survey_id', 'avg_home_score', 'avg_home_score_returned',
                  'standard_deviation_homes', 'standard_deviation_homes_returned', 'max_score_home',
                  'max_score_home_returned', 'min_score_home', 'min_score_home_returned', 'hum_homes')


class SurveyResultsIterationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SurveyResultIterationResource


admin.site.register(SurveyResultsIteration, SurveyResultsIterationAdmin)