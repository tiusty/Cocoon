from django.conf.urls import url, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'itinerary', views.ItineraryViewset, base_name='itinerary')
# router.register(r'visitTime', views.VisitTimeViewset, base_name='visitTime')
router.register(r'itineraryClient', views.ItineraryClientViewSet, base_name='itineraryClient')
router.register(r'itineraryAgent', views.ItineraryAgentViewSet, base_name='itineraryAgent')
router.register(r'itineraryMarket', views.ItineraryMarketViewSet, base_name='itineraryMarket')
router.register(r'itineraryDuration', views.ClientItineraryCalculateDuration, base_name='itineraryDuration')
router.register(r'itineraryClientStatus', views.RetrieveClientItineraryStatus, base_name='itineraryClientStatus')

app_name = 'scheduler'
urlpatterns = [
    url(r'^agentSchedulerPortal/', views.AgentSchedulerPortalView.as_view(), name="agentSchedulerPortal"),
    url(r'^agentSchedulerMarketplace/', views.AgentSchedulerMarketplaceView.as_view(), name="agentSchedulerMarketplace"),
    url(r'^clientScheduler', views.ClientSchedulerView.as_view(), name="clientScheduler"),
    url(r'^itineraryPage/(?P<itinerary_slug>.*)/$', views.ItineraryFileView.as_view(), name="itineraryFile"),

    # AJAX requests below
    url(r'^unscheduleItinerary/$', views.unschedule_itinerary, name="unscheduleItinerary"),
    url(r'^updateVisitTime/$', views.update_visit_time, name="updateVisitTime"),

    # Api
    url(r'^api/', include(router.urls))
]
