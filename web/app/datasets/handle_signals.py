"""
Script that handles Signals from "signals" API, sends messages to external services.

Version 1:
- request signals from "signal" API
- loop over them:
    - add to local Signals database if not there already
    - send signal if needed, update status in DB
- all this is controlled by Jenkins (so this program will be a manage.py command)

Possible upgrades:
- provide a convenient endpoint for the signal API to check which messages were sent
- allow signal API to post a message to process
- add a proper task queue (like Celery)
"""
# Assumptions:
# 1) Each signal will be sent to 1 API at most (underlies both table design and
#    routing implementation.


import os
import datetime
import logging

import requests
from django.conf import settings
from django.utils import timezone

from datasets.models import MessageLog
from datasets.external.base import get_handler

# -- setup logging --
LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -- Datapunt internal Signalen in Amsterdam API endpoints --
#    note: should be set by Ansible or docker-compose.yml
SIGNALS_API_BASE = os.getenv('SIGNALS_API_BASE', 'https://acc.api.data.amsterdam.nl')


def _get_session_with_retries():
    """
    Get a requests Session that will retry 5 times on a number of HTTP 500 statusses.
    """
    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=True
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    return session


def _batch_signals(signals):
    """
    Access the Signalen in Amsterdam API, retrieve signals.
    """
    next_page = SIGNALS_API_BASE + '/signal/'

    with _get_session_with_retries() as session:
        result = session.get(next_page)
        yield result.json()['results']

        next_page = results.json()['_links']['next']['href']
        if next_page == None:
            raise StopIteration


def _call_external_apis(signals):
    """
    Call external APIs for each of the signals.

    Note signals are expected as dictionaries, not objects.
    """
    for s in signals:
        # Check local database to see whether this signal was alreay sent to
        # the relevant external API (if so skip, else update local database).
        try:
            entry = MessageLog.objects.get(signal_id=s['signal_id'])
        except MessageLog.DoesNotExist:
            logger.debug('Creating entry for {}.'.format(s['signal_id']))
            entry = MessageLog(
                signal_id=s['signal_id'],
                t_entered=timezone.now()
            )
            entry.save()
        else:
            logger.debug('Retrieved entry for {}.'.format(s['signal_id']))
            if entry.is_sent:
                continue

        # Send the signal to the correct API.
        handler = get_handler(s)
        success, status = handler.handle(s)

        # Save the status to our local database.
        entry.is_sent = success
        entry.status = status
        entry.t_sent = timezone.now()
        entry.handler_name = handler.name

        entry.save()


def handle_signals():
    """
    Entry point (called via manage.py), retrieve and handle signals.
    """
    for signals in _batch_signals():
        _call_external_apis(signals)
