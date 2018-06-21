"""
Test suite for Sigmax message generation.
"""
import logging
import time
import datetime
from unittest import mock
from lxml import etree

from django.test import TestCase

from datasets.external import sigmax


LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logging.disable(logging.NOTSET)
logger = logging.getLogger(__name__)

class TestSigmaxHelpers(TestCase):
    def test_format_datetime(self):
        dt = datetime.datetime(2018, 7, 9, 10, 0, 30)
        self.assertEqual(
            sigmax._format_datetime(dt),
            '20180709100030'
        )

        dt = datetime.datetime(2018, 7, 9, 22, 0, 30)
        self.assertEqual(
            sigmax._format_datetime(dt),
            '20180709220030'
        )

    def test_format_date(self):
        dt = datetime.datetime(2018, 7, 9, 10, 59, 34)
        self.assertEqual(
            sigmax._format_date(dt),
            '20180709'
        )

    def test_wrong_type(self):
        with self.assertRaises(AttributeError):
            sigmax._format_datetime(None)
        with self.assertRaises(AttributeError):
            t = time.time()
            sigmax._format_datetime(t)

        with self.assertRaises(AttributeError):
            sigmax._format_date(None)
        with self.assertRaises(AttributeError):
            t = time.time()
            sigmax._format_date(t)


class TestGenerateStufMessage(TestCase):
    def test_is_xml(self):
        signal = {'signal_id': 'ABACADABRA'}
        xml = sigmax._generate_stuf_message(signal)

        try:
            root = etree.fromstring(xml)
        except:
            self.fail('Cannot parse STUF message as XML')

    def test_escaping(self):
        poison = {'signal_id': '<poison>tastes nice</poison>'}
        msg = sigmax._generate_stuf_message(poison)
        self.assertTrue('<poison>' not in msg)


def show_args_kwargs(*args, **kwargs):
    return args, kwargs


class TestSendStufMessage(TestCase):
    def test_no_environment_variables(self):
        # Check that missing enviroment variables for server and auth token
        # raises an error when a message is sent.
        env_override = {'SIGMAX_AUTH_TOKEN': '', 'SIGMAX_SERVER': ''}

        with mock.patch.dict('os.environ', env_override):
            with self.assertRaises(sigmax.ServiceNotConfigured):
                sigmax._send_stuf_message('TEST BERICHT')


    @mock.patch('requests.post', side_effect=show_args_kwargs)
    def test_send_message(self, request_post_mock):
        # Check that headers are set correctly when sending an STUF message.
        message = 'TEST BERICHT'
        env_override = {
            'SIGMAX_AUTH_TOKEN': 'SLEUTEL',
            'SIGMAX_SERVER': 'TESTSERVER',
        }

        with mock.patch.dict('os.environ', env_override):
            args, kwargs = sigmax._send_stuf_message(message)

            self.assertEquals(request_post_mock.called, 1)
            self.assertEquals(kwargs['url'], 'TESTSERVER')
            self.assertEquals(
                kwargs['headers']['Authorization'],
                'Basic SLEUTEL'
            )
            self.assertEquals(
                kwargs['headers']['SOAPAction'],
                'http://www.egem.nl/StUF/sector/zkn/0310/CreeerZaak_Lk01'
            )
            self.assertEquals(
                kwargs['headers']['Content-Type'],
                'text/xml; charset=UTF-8'
            )
            self.assertEquals(
                bytes(len(message)),
                kwargs['headers']['Content-Length']
            )



