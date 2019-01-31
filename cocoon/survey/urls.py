from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'rentSurvey', views.RentSurveyViewSet, base_name='user_survey')
router.register(r'rentResult', views.RentResultViewSet, base_name='survey-result')
router.register(r'tenants', views.TenantViewSet, base_name='tenants-update')

app_name = 'survey'
urlpatterns = [
    url(r'^rent/$', views.RentingSurveyTemplate.as_view(), name="rentingSurvey"),
    url(r'^rent/(?P<survey_url>.*)/$', views.RentingResultTemplate.as_view(), name="rentSurveyResult"),

    # Api
    url(r'^api/', include(router.urls))
]
