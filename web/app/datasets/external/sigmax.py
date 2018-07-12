"""
Send messages to the external Sigmax API.

Minimal implementation based on work by Maarten Sukel and Sigmax technical
documentation. More specifically it implements sections 3.1, 3.1.1, 3.3, 
3.3.1) from "Technische Documentatie Zaak- en Documentservices koppelvlak
CityControl t.b.v. Zaakgericht werken" version 1.1.0, 2018-05-02.

SOAP actions:
- http://www.egem.nl/StUF/sector/zkn/0310/CreeerZaak_Lk01
- http://www.egem.nl/StUF/sector/zkn/0310/VoegZaakdocumentToe_Lk01

This module contains the code to register a "Zaak" with Sigmax / City
Control and follow it up by sending a PDF with extra information from the
SIA system.


"""
import os
import logging
import datetime
import uuid
import requests
from dateutil.parser import parse
from xml.sax.saxutils import escape

from datasets.external.base import BaseAPIHandler
from datasets.external.sigmax_pdf import _generate_pdf
from datasets.external.sigmax_xml_templates import CREER_ZAAK
from datasets.external.sigmax_xml_templates import VOEG_ZAAK_DOCUMENT_TOE

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -- format string for message generation --

PLACEHOLDER_STRING = ''

# -- helper functions --
def _format_datetime(dt):
    """Format datetime as YYYYMMDDHHMMSS."""
    return dt.strftime('%Y%m%d%H%M%S')


def _format_date(dt):
    """Format date as YYYYMMDD."""
    return dt.strftime('%Y%m%d')


class ServiceNotConfigured(Exception):
    pass


# -- functions that generate or send messages --

def _generate_creeer_zaak_lk01_message(signal):
    """
    Generate XML for Sigmax CreeerZaak_Lk01
    """
    # convert the ISO8601 datetime strings (from JSON data) to datetime objects
    created_at = parse(signal['created_at'])
    incident_date_start = parse(signal['incident_date_start'])
    incident_date_end = parse(signal['incident_date_end'])

    return CREER_ZAAK.format(**{
        'PRIMARY_KEY': escape(signal['signal_id']),
        'OMSCHRIJVING': escape('Dit is een test bericht'),
        'TIJDSTIPBERICHT': escape(_format_datetime(created_at)),
        'STARTDATUM': escape(_format_date(incident_date_start)),
        'REGISTRATIEDATUM': escape(_format_date(created_at)),
        'EINDDATUMGEPLAND': escape(_format_date(incident_date_end)),
        'OPENBARERUIMTENAAM': escape(signal['location']['address']['openbare_ruimte']),
        'HUISNUMMER': escape(signal['location']['address']['huisnummer']),
        'POSTCODE': escape(signal['location']['address']['postcode']),
        'X': escape(str(signal['location']['geometrie']['coordinates'][0])),
        'Y': escape(str(signal['location']['geometrie']['coordinates'][1])),
    })


def _generate_voeg_zaak_document_toe_lk01(signal, pdf_buffer=None):
    """
    Generate XML for Sigmax VoegZaakdocumentToe_Lk01
    """
    encoded_pdf = _generate_pdf(signal)
    msg = VOEG_ZAAK_DOCUMENT_TOE.format(**{
        'ZKN_UUID': escape(signal['signal_id']),
        'DOC_UUID': escape(str(uuid.uuid4())),
        'PDF_DATA': encoded_pdf.decode('utf-8'),
        'DOC_TYPE': 'PDF',
        'DOC_TYPE_LOWER': 'pdf',
        'FILE_NAME': 'info-' + signal['signal_id'] + '.pdf'
    })

    return msg


def _send_stuf_message(stuf_msg, soap_action):
    """
    Send a STUF message to the server that is configured.
    """
    # Grab credentials from environment (assumption, these are set for
    # either testing or production --- not configurable at run time).
    SIGMAX_AUTH_TOKEN = os.getenv('SIGMAX_AUTH_TOKEN', None)
    SIGMAX_SERVER = os.getenv('SIGMAX_SERVER', None)

    if not SIGMAX_AUTH_TOKEN or not SIGMAX_SERVER:
        msg = 'SIGMAX_AUTH_TOKEN or SIGMAX_SERVER not configured.'
        raise ServiceNotConfigured(msg)

    # Prepare our request to Sigmax
    encoded = stuf_msg.encode('utf-8')
    headers = {
        'SOAPAction': soap_action,
        'Content-Type': 'text/xml; charset=UTF-8',
        'Authorization': 'Basic ' + SIGMAX_AUTH_TOKEN,
        'Content-Length': bytes(len(encoded))
    }

    # Send our message to Sigmax
    response = requests.post(
        url=SIGMAX_SERVER,
        headers=headers,
        data=encoded,
        verify=False
    )

    # We return the response object so that we can check the response from
    # the external API handler.
    return response


# -- Sigmax API Handler --
# Note: the SigmaxHandler below does not yet implement the can_handle method
# because at present no clear specs are available for the message routing.
# TODO: implement can_handle method on SigmaxHandler

class SigmaxHandler(BaseAPIHandler):
    def handle(self, signal):
        soap_action = 'http://www.egem.nl/StUF/sector/zkn/0310/CreeerZaak_Lk01'
        msg = _generate_creeer_zaak_lk01_message(signal)
        response = _send_stuf_message(msg, soap_action)
        logger.info('Sent {}'.format(soap_action))
        logger.info('Received:\n{}'.format(response.text))

        soap_action = 'http://www.egem.nl/StUF/sector/zkn/0310/VoegZaakdocumentToe_Lk01'
        msg = _generate_voeg_zaak_document_toe_lk01(signal)

## -- uncomment this to get the message dumped to a file in the local directory --
##        DIR = os.path.split(__file__)[0]
##        with open(os.path.join(DIR, 'dumped-' + str(uuid.uuid4()) + '.xml'), 'wb') as f:
##            f.write(msg.encode('utf-8'))

        response = _send_stuf_message(msg, soap_action)
        logger.info('Sent {}'.format(soap_action))
        logger.info('Received:\n{}'.format(response.text))
