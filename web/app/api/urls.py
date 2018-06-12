from django.conf.urls import url, include
from api import views

router = views.SignalsExportAPIRouter()
router.register(
    'messagelog', views.MessageLogViewSet, base_name='messagelog')

urlpatterns = [
    url(r'^', include(router.urls)),
]
