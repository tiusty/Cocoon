from django.conf.urls import url

from . import views

app_name = 'userAuth'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginPage, name='loginPage'),
    url(r'^register/$', views.SignUpView.as_view(), name='signup'),
    url(r'^register/hunter/', views.ApartmentHunterSignupView.as_view(), name='hunter_signup'),
    url(r'^register/broker/', views.BrokerSignupView.as_view(), name='broker_signup'),
    url(r'^password_change/$', views.change_password, name='change_password'),
    url(r'^logout/$', views.logoutPage, name='logoutPage'),
    url(r'^profile$', views.user_profile, name='user_profile'),
    url(r'^surveys', views.user_surveys, name='user_surveys'),
]
