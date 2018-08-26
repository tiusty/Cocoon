from django.conf.urls import url

from . import views

app_name = 'survey'
urlpatterns = [
    url(r'^rent/$', views.renting_survey, name="rentingSurvey"),
    # url(r'^buy/$', views.buying_survey, name="buyingSurvey"),
    url(r'^visits/$', views.visit_list, name="visitList"),
    url(r'^result/rent/$', views.survey_result_rent, name="rentSurveyResult"),
    url(r'^result/rent/(?P<survey_slug>.*)/$', views.survey_result_rent, name="rentSurveyResult"),
    # Ajax requests
    url(r'^setFavorite/$', views.set_favorite, name="setFavorite"),
    url(r'^deleteSurvey/$', views.delete_survey, name="surveyDelete"),
    url(r'^setVisitHome/$', views.set_visit_house, name="setVisitHouse"),
    url(r'^deleteVisitHome/$', views.delete_visit_house, name="deleteVisitHouse"),
]
