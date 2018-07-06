import os
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from datasets.external.send_example import send_example


# Known to still be problematic, work in progress
class Command(BaseCommand):
    help = 'Send a message to "Sigmax" as a manual test.'

    def add_arguments(self, parser):
        parser.add_argument(
            'example', nargs='?', help='Which message to send 1-4', default=1) 

    def handle(self, *args, **options):
        self.stdout.write('Sending a message to Sigmax.')
        r = send_example(options['example'])
        self.stdout.write('response status code: {}'.format(r.status_code))
        self.stdout.write('Logging response.text :')
        self.stdout.write(r.text)
