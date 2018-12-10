from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'itinerary', views.ItineraryClientViewSet, base_name='itinerary')
router.register(r'itineraryAgent', views.ItineraryAgentViewSet, base_name='itineraryAgent')
router.register(r'itineraryMarket', views.ItineraryMarketViewSet, base_name='itineraryMarket')

app_name = 'scheduler'
urlpatterns = [
    url(r'^agentSchedulerPortal/', views.AgentSchedulerPortal.as_view(), name="agentSchedulerPortal"),
    url(r'^agentSchedulerMarketplace/', views.AgentSchedulerMarketplace.as_view(), name="agentSchedulerMarketplace"),
    url(r'^clientScheduler', views.ClientScheduler.as_view(), name="clientScheduler"),

    # AJAX requests below
    url(r'^unscheduleItinerary/$', views.unschedule_itinerary, name="unscheduleItinerary"),

    # Api
    url(r'^api/', include(router.urls))
]
