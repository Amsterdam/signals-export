from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import routers
from datapunt_api.rest import DatapuntViewSet, HALPagination

from api.serializers import MessageLogSerializer
from datasets.models import MessageLog


class AuthViewSet():
    def check_permissions(self, request):
        scope = 'SIG/ALL'
        if not request.is_authorized_for(scope):
            self.permission_denied(
                request, message=getattr(scope, 'message', None)
            )
        return super(AuthViewSet, self).check_permissions(request)


# --- general ---

class SignalsExportAPIView(routers.APIRootView):
    """
    API endpoints for signals-export service.
    """


class SignalsExportAPIRouter(routers.DefaultRouter):
    APIRootView = SignalsExportAPIView


# --- specific ---

class MessageLogViewSet(AuthViewSet, DatapuntViewSet):
    serializer_class = MessageLogSerializer
    serializer_detail_class = MessageLogSerializer

    queryset = MessageLog.objects.order_by('-signal_id').all()
