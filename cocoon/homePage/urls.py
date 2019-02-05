from django.conf.urls import url

from . import views

app_name = 'homePage'
urlpatterns = [
    url(r'^$', views.LandingPage.as_view(), name='index'),
]
