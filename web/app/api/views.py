from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import routers
from datapunt_api.rest import DatapuntViewSet, HALPagination

from api.serializers import ExternalAPISerializer
from api.serializers import SignalSerializer
from datasets.models import ExternalAPI
from datasets.models import Signal


# --- general ---

class SignalsExportAPIView(routers.APIRootView):
    """
    API endpoints for signals-export service.
    """


class SignalsExportAPIRouter(routers.DefaultRouter):
    APIRootView = SignalsExportAPIView


# --- specific ---

class ExternalAPIViewSet(DatapuntViewSet):
    serializer_class = ExternalAPISerializer
    serializer_detail_class = ExternalAPISerializer

    queryset = ExternalAPI.objects.order_by('name').all()


class SignalViewSet(DatapuntViewSet):
    serializer_class = ExternalAPISerializer
    serializer_detail_class = ExternalAPISerializer

    queryset = Signal.objects.order_by('-signal_id').all()
