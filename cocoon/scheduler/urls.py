from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'itinerary', views.ItineraryViewset, base_name='itinerary')
router.register(r'itineraryClient', views.ItineraryClientViewSet, base_name='itineraryClient')
router.register(r'itineraryAgent', views.ItineraryAgentViewSet, base_name='itineraryAgent')
router.register(r'itineraryMarket', views.ItineraryMarketViewSet, base_name='itineraryMarket')
router.register(r'itineraryDuration', views.ClientItineraryCalculateDuration, base_name='itineraryDuration')

app_name = 'scheduler'
urlpatterns = [
    url(r'^agentSchedulerOld/', views.agent_scheduler, name="agentSchedulerOld"),
    url(r'^agentScheduler/', views.AgentSchedulerView.as_view(), name="agentScheduler"),
    url(r'^myToursOld/', views.view_tours, name="myTours"),
    url(r'^clientScheduler', views.ClientSchedulerView.as_view(), name="clientScheduler"),

    # AJAX requests below
    url(r'^claimItinerary/$', views.claim_itinerary, name="claimItinerary"),
    url(r'^selectStartTime/$', views.select_start_time, name="selectStartTime"),
    url(r'^unscheduleItinerary/$', views.unschedule_itinerary, name="unscheduleItinerary"),

    # Api
    url(r'^api/', include(router.urls))
]