"""
Send messages to the external Sigmax API.

Minimal implementation based on work by Maarten Sukel.
"""
import logging
import datetime

from datasets.external.base import BaseAPIHandler

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -- helper functions --
def _format_datetime(dt):
    """Format datetime as YYYYMMDDHHMMSS."""
    return dt.strftime('%Y%m%d%H%M%S')


def _format_date(dt):
    """Format date as YYYYMMDD."""
    return dt.strftime('%Y%m%d')


# -- functions that generate or send messages --

def _generate_stuf_message(signal):
    """
    Generate the XML needed for Sigmax.
    """
    pass


def _send_stuf_message(stuf_msg):
    """
    Send a STUF message to the server that is configured.
    """
    pass


# -- Sigmax API Handler --

class SigmaxHandler(BaseAPIHandler):
    def handle(self, signal):
        pass

    def can_handle(self, signal):
        pass
