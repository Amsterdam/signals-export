from django.conf.urls import url, include
from api import views

router = views.SignalsExportAPIRouter()
router.register(
    'signals', views.SignalViewSet, base_name='signals')
router.register(
    'external_apis', views.ExternalAPIViewSet, base_name='external_apis')

urlpatterns = [
    url(r'^', include(router.urls)),
]
