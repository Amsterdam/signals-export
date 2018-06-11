from django.conf.urls import include
from django.urls import path
from api import urls as api_urls

urlpatterns = [
    path('signals-export/', include(api_urls))
]
