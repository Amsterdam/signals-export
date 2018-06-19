import json
import datetime

from django.test import TestCase
from django.utils import timezone
from django.test.utils import override_settings
import pytz

from datasets import handle_signals
from datasets.models import MessageLog
from datasets.external.base import reset_handlers

SIGNAL_PLACEHOLDERS = json.loads("""
[
    {
        "signal_id": "1"
    },
    {
        "signal_id": "2"
    },
    {
        "signal_id": "4"
    }
]
""")


class TestSignalHandling(TestCase):
    def setUp(self):
        reset_handlers()
        MessageLog.objects.create(
            signal_id='1',
            t_entered=timezone.now(),
            t_sent=timezone.now(),
            handler_name='some-handler',
            status='200',
            is_sent=True
        )

    def test_call_external_apis(self):
        signals = SIGNAL_PLACEHOLDERS

        handle_signals._call_external_apis(signals)
        self.assertEquals(MessageLog.objects.count(), 3)

        handle_signals._call_external_apis(signals)
        self.assertEquals(MessageLog.objects.count(), 3)

