from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'homeTypes', views.HomeTypeViewSet, base_name='home_types')

app_name = 'houseDatabase'
urlpatterns = [
    # Api
    url(r'^api/', include(router.urls))
]
