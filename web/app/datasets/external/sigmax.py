"""
Send messages to the external Sigmax API.

Minimal implementation based on work by Maarten Sukel.
"""
import os
import logging
import datetime
import requests
from xml.sax.saxutils import escape

from datasets.external.base import BaseAPIHandler

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -- format string for message generation --

PLACEHOLDER_STRING = ''
TEMPLATE =\
u"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
       <soap:Body>
          <ZKN:zakLk01 xmlns:ZKN="http://www.egem.nl/StUF/sector/zkn/0310" xmlns:BG="http://www.egem.nl/StUF/sector/bg/0310" xmlns:mime="http://schemas.xmlsoap.org/wsdl/mime/" xmlns:gml="http://www.opengis.net/gml" xmlns:bag="http://www.vrom.nl/bag/0120" xmlns:soap12="http://schemas.xmlsoap.org/wsdl/soap12/" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:StUF="http://www.egem.nl/StUF/StUF0301" xmlns:tns="http://www.circlesoftware.nl/verseon/mng/webservice/2012" xmlns:tm="http://microsoft.com/wsdl/mime/textMatching/" xmlns:http="http://schemas.xmlsoap.org/wsdl/http/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:xlink="http://www.w3.org/1999/xlink">
             <ZKN:stuurgegevens>
                <StUF:berichtcode>Lk01</StUF:berichtcode>
                <StUF:zender>
                   <StUF:organisatie>AMS</StUF:organisatie>
                   <StUF:applicatie>VER</StUF:applicatie>
                </StUF:zender>
                <StUF:ontvanger>
                   <StUF:organisatie>SMX</StUF:organisatie>
                   <StUF:applicatie>CTC</StUF:applicatie>
                </StUF:ontvanger>
                <StUF:referentienummer>{PRIMARY_KEY}</StUF:referentienummer>
                <StUF:tijdstipBericht>{TIJDSTIPBERICHT}</StUF:tijdstipBericht>
                <StUF:entiteittype>ZAK</StUF:entiteittype>
             </ZKN:stuurgegevens>
             <ZKN:parameters>
                <StUF:mutatiesoort>T</StUF:mutatiesoort>
                <StUF:indicatorOvername>V</StUF:indicatorOvername>
             </ZKN:parameters>
             <ZKN:object StUF:entiteittype="ZAK" StUF:sleutelGegevensbeheer="" StUF:verwerkingssoort="T">
                <ZKN:identificatie>{PRIMARY_KEY}</ZKN:identificatie>
                <ZKN:omschrijving>{OMSCHRIJVING}</ZKN:omschrijving>
                <ZKN:startdatum>{STARTDATUM}</ZKN:startdatum>
                <ZKN:registratiedatum>{REGISTRATIEDATUM}</ZKN:registratiedatum>
                <ZKN:einddatumGepland>{EINDDATUMGEPLAND}</ZKN:einddatumGepland>
                <ZKN:archiefnominatie>N</ZKN:archiefnominatie>
                <ZKN:zaakniveau>1</ZKN:zaakniveau>
                <ZKN:deelzakenIndicatie>N</ZKN:deelzakenIndicatie>
                <StUF:extraElementen>
                   <StUF:extraElement naam="Ycoordinaat">{EINDDATUMGEPLAND}</StUF:extraElement>
                   <StUF:extraElement naam="Xcoordinaat">{EINDDATUMGEPLAND}</StUF:extraElement>
                </StUF:extraElementen>
                <ZKN:isVan StUF:entiteittype="ZAKZKT" StUF:verwerkingssoort="T">
                   <ZKN:gerelateerde StUF:entiteittype="ZKT" StUF:sleutelOntvangend="1" StUF:verwerkingssoort="T">
                      <ZKN:omschrijving>Uitvoeren controle</ZKN:omschrijving>
                      <ZKN:code>2</ZKN:code>
                   </ZKN:gerelateerde>
                </ZKN:isVan>
                <ZKN:heeftBetrekkingOp StUF:entiteittype="ZAKOBJ" StUF:verwerkingssoort="T">
                   <ZKN:gerelateerde>
                      <ZKN:adres StUF:entiteittype="AOA" StUF:verwerkingssoort="T">
                         <BG:wpl.woonplaatsNaam>Amsterdam</BG:wpl.woonplaatsNaam>
                         <BG:gor.openbareRuimteNaam>{OPENBARERUIMTENAAM}</BG:gor.openbareRuimteNaam>
                         <BG:huisnummer>{HUISNUMMER}</BG:huisnummer>
                         <BG:huisletter StUF:noValue="geenWaarde" xsi:nil="true"/>
                         <BG:postcode>{POSTCODE}</BG:postcode>
                      </ZKN:adres>
                   </ZKN:gerelateerde>
                </ZKN:heeftBetrekkingOp>
             </ZKN:object>
          </ZKN:zakLk01>
       </soap:Body>
    </soap:Envelope>"""


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

def _generate_stuf_message(signal):
    """
    Generate the XML needed for Sigmax.
    """
    return TEMPLATE.format(**{
        'PRIMARY_KEY': escape(signal['signal_id']),
        'OMSCHRIJVING': escape('Dit is een test bericht'),
        'TIJDSTIPBERICHT': escape(PLACEHOLDER_STRING),
        'STARTDATUM': escape(PLACEHOLDER_STRING),
        'REGISTRATIEDATUM': escape(PLACEHOLDER_STRING),
        'EINDDATUMGEPLAND': escape(PLACEHOLDER_STRING),
        'OPENBARERUIMTENAAM': escape(PLACEHOLDER_STRING),
        'HUISNUMMER': escape(PLACEHOLDER_STRING),
        'POSTCODE': escape(PLACEHOLDER_STRING),
    })


def _send_stuf_message(stuf_msg):
    """
    Send a STUF message to the server that is configured.
    """
    # Grab credentials from environment (assumption, these are set for
    # either testing or production --- not configurable at run time).
    SIGMAX_AUTH_TOKEN = os.getenv('SIGMAX_AUTH_TOKEN', None)
    SIGMAX_SERVER = os.getenv('SIGMAX_SERVER', None)
    logger.debug('SIGMAX_SERVER: {}'.format(SIGMAX_SERVER))
    logger.debug('SIGMAX_AUTH_TOKEN: {}'.format(SIGMAX_AUTH_TOKEN))

    if not SIGMAX_AUTH_TOKEN or not SIGMAX_SERVER:
        msg = 'SIGMAX_AUTH_TOKEN or SIGMAX_SERVER not configured.'
        raise ServiceNotConfigured(msg)

    # Prepare our request to Sigmax
    encoded = stuf_msg.encode('utf-8')
    headers = {
        'SOAPAction': 'http://www.egem.nl/StUF/sector/zkn/0310/CreeerZaak_Lk01',
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

class SigmaxHandler(BaseAPIHandler):
    def handle(self, signal):
        pass

    def can_handle(self, signal):
        pass # TODO: integrate with "signals" API
