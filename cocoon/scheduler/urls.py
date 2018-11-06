from django.conf.urls import url

from . import views

app_name = 'scheduler'
urlpatterns = [
    url(r'^agentScheduler/', views.agent_scheduler, name="agentScheduler"),
    url(r'^myTours/', views.view_tours, name="myTours"),
    # AJAX requests below
    url(r'^claimItinerary/$', views.claim_itinerary, name="claimItinerary"),
    url(r'^selectStartTime/$', views.select_start_time, name="selectStartTime"),
    url(r'^unscheduleItinerary/$', views.unschedule_itinerary, name="unscheduleItinerary"),
]