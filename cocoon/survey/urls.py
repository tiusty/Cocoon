from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'userSurveys', views.RentSurveyViewSet, base_name='user_survey')

app_name = 'survey'
urlpatterns = [
    url(r'^rent/$', views.RentingSurvey.as_view(), name="rentingSurvey"),
    url(r'^rentReact/$', views.RentingSurvey.as_view(template_name='survey/reactRentingSurvey.html'), name="rentingSurveyReact"),
    url(r'^rent/(?P<survey_url>.*)/$', views.RentingResultSurvey.as_view(), name="rentSurveyResult"),

    # Ajax requests
    url(r'^setFavorite/$', views.set_favorite, name="setFavorite"),
    url(r'^deleteSurvey/$', views.delete_survey, name="surveyDelete"),
    url(r'^setVisitHome/$', views.set_visit_house, name="setVisitHouse"),
    url(r'^deleteVisitHome/$', views.delete_visit_house, name="deleteVisitHouse"),
    url(r'^check_pre_tour_documents/$', views.check_pre_tour_documents, name="checkPretourDocuments"),
    url(r'^resend_pre_tour_documents/$', views.resend_pre_tour_documents, name="resendPretourDocuments"),

    # Api
    url(r'^api/', include(router.urls))
]
