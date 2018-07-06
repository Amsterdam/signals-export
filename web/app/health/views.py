import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection

from signalsexport.env_vars import required_env_vars_are_present

try:
    # noinspection PyUnresolvedReferences
    from django.apps import apps

    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

from django.http import HttpResponse

try:
    print('Grabbing', settings.HEALTH_MODEL)
    model = get_model(settings.HEALTH_MODEL)
except:  # noqa E722
    raise ImproperlyConfigured(
        "settings.HEALTH_MODEL {} doesn't resolve to "
        "a useable model".format(settings.HEALTH_MODEL)
    )


log = logging.getLogger(__name__)


def health(request):
    # check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            assert cursor.fetchone()
    except:  # noqa E722
        log.exception("Database connectivity failed")
        return HttpResponse(
            "Database connectivity failed",
            content_type="text/plain", status=500
        )

    healthy, error_msg = required_env_vars_are_present():
    if healthy:
        msg = "Service misconfigured: not all required env variables are set"
        log.exception('{}\n{}'.format(msg, error_msg))
        return HttpResponse(msg, content_type="text/plain", status=500)

    return HttpResponse(
        "Connectivity OK", content_type="text/plain", status=200)


def check_data(request):

    count = model.objects.count()
    if count < 2:
        return HttpResponse(
            "Too few items in the database",
            content_type="text/plain", status=500
        )

    return HttpResponse(
        f"Data OK {count} {model.__name__}",
        content_type="text/plain", status=200)
