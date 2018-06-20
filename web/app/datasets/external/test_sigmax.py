"""
Test suite for Sigmax message generation.
"""
import logging
import time
import datetime

from django.test import TestCase

from datasets.external import sigmax


LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
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
