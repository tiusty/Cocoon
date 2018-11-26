from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'commuteTypes', views.CommuteTypeViewSet, base_name='commute_types')

app_name = 'commutes'
urlpatterns = [
    # Api
    url(r'^api/', include(router.urls))
]
