from django.conf.urls import url

from . import views

app_name = 'userAuth'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginPage, name='loginPage'),
    url(r'^register/$', views.registerPage, name='registerPage'),
    url(r'^logout/$', views.logoutPage, name='logoutPage'),
    url(r'^userProfile/$', views.ProfilePage, name='profilePage'),
    url(r'^userProfile/(?P<defaultPage>(profile|rentSurvey|buySurvey|favorites))/$', views.ProfilePage, name='profilePage')
]
