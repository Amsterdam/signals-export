from django.conf.urls import url, include
from api import views

router = views.SignalsExportAPIRouter()
router.register(
    'signal', views.SignalViewSet, base_name='signal')
router.register(
    'external_api', views.ExternalAPIViewSet, base_name='external_api')

urlpatterns = [
    url(r'^', include(router.urls)),
]
