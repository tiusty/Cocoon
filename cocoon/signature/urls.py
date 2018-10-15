from django.conf.urls import url

from . import views

app_name = 'signature'
urlpatterns = [
    url(r'^$', views.signature_page, name="signaturePage"),
]
