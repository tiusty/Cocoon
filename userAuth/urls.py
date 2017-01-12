from django.conf.urls import url

from . import views

app_name = 'userAuth'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginPage, name='loginPage'),
    url(r'^register/$', views.registerPage, name='registerPage'),
    url(r'^logout/$', views.logoutPage, name='logoutPage')
]
