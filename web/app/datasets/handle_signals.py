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


def _route_signals(signal):
    pass # use external_api property to route


def handle_signals():
    pass
