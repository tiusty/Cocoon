# Django Modules
from django.conf.urls import url, include

# Rest Framework Modules
from rest_framework import routers

# App modules
from . import views

router = routers.DefaultRouter()
router.register(r'hunterDocManager', views.HunterDocManagerViewset, base_name='HunterDocManager')
router.register(r'hunterDoc', views.HunterDocViewset, base_name='HunterDoc')
router.register(r'hunterDocTemplate', views.HunterDocTemplateViewset)

app_name = 'signature'
urlpatterns = [
    url(r'^$', views.SignaturePage.as_view(), name="signaturePage"),

    # Api
    url(r'^api/', include(router.urls))
]
