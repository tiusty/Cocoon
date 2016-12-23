from django.conf.urls import url

from . import views

app_name = 'survey'
urlpatterns = [
    url(r'^rent/$', views.renting_survey, name="rentingSurvey"),
    url(r'^buy/$', views.buying_survey, name="buyingSurvey"),
    url(r'^result/(?P<survey_type>(rent|buy))/$', views.survey_result, name="surveyResult"),
]
