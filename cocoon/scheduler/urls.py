from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'itinerary', views.ItineraryViewSet, base_name='itinerary')
router.register(r'itineraryDuration', views.ClientSchedulerItineraryDuration, base_name='itineraryDuration')

app_name = 'scheduler'
urlpatterns = [
    url(r'^agentScheduler/', views.agent_scheduler, name="agentScheduler"),
    url(r'^myTours/', views.view_tours, name="myTours"),
    url(r'^clientScheduler', views.ClientSchedulerView.as_view(), name="clientScheduler"),

    # AJAX requests below
    url(r'^claimItinerary/$', views.claim_itinerary, name="claimItinerary"),
    url(r'^selectStartTime/$', views.select_start_time, name="selectStartTime"),
    url(r'^unscheduleItinerary/$', views.unschedule_itinerary, name="unscheduleItinerary"),

    # Api
    url(r'^api/', include(router.urls))
]