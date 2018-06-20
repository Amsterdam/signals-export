from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import urls as api_urls
from health import urls as health_urls

schema_view = get_schema_view(
    openapi.Info(
        title='signals-export API',
        description='Communication to external systems for the "Signalen in Amsterdam" project.',
        contact=openapi.Contact(email="datapunt@amsterdam.nl"),
        default_version='v1',
        ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Swagger / OpenAPI
    re_path(
        r'^signals-export/swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=None),
        name='schema-json'
    ),
    re_path(
        r'^signals-export/swagger/$',
        schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^signals-export/redoc/$',
        schema_view.with_ui('redoc', cache_timeout=None),
        name='schema-redoc'
    ),

    # health checks for deploy / orchestration
    path('status/', include(health_urls)),

    # The signals-export API endpoints
    path('signals-export/', include(api_urls)),
]
