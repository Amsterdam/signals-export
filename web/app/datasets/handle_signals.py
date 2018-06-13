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
import os

import requests

from datasets import models


API_BASE = 'https://acc.api.data.amsterdam.nl/signals'


def _get_session_with_retries():
    """
    Get a requests Session that will retry some set number of times.
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


class BaseExternalAPIHandler():
    external_api = None

    def handle(self, signal):
        """
        Given a signal call out to an external API.
        """
        # Expected return value a tuple of (success, status)
        # Make sure that any Exceptions caused by the interactions with external
        # APIs are silenced.
        raise NotImplentedError('Subclass {} to provide an implementation.'.format(self.__class__))


def _get_handler(signal):
    pass


def _batch_signals(signals):
    next_page = API_BASE + '/signal/'

    with _get_session_with_retries() as session:
        result = session.get(next_page)
        yield result.json()['results']

        next_page = results.json()['_links']['next']['href']
        if next_page == None:
            raise StopIteration


def _call_external_apis(signals):
    """
    Call external APIs for each of the signals.
    """
    for s in signals:
        try:
            entry = MessageLog.objects.get(s.signal_id)
        except MessageLog.DoesNotExist:
            entry = MessageLog(
                signal_id=s.signal_id,
                t_entered=datetime.datetime.now()
            )
            entry.save()
        else:
            if s.is_sent:
                continue

        handler = _get_handler(s)
        success, status = handler.handle(s)

        entry.success = success
        entry.status = status
        entry.t_sent = datetime.datetime.now()
        entry.external_api = handler.external_api

        entry.save()


def handle_signals():
    for signals in _batch_signals():
        _call_external_apis(signals)
