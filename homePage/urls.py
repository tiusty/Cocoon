from django.conf.urls import url

from . import views

app_name = 'homePage'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contactPage, name='contactPage'),
]
