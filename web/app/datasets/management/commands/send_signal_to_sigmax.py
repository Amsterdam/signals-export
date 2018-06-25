import os
import uuid

from django.core.management.base import BaseCommand, CommandError

from datasets.external.sigmax import _generate_stuf_message, _send_stuf_message


# Known to still be problematic, work in progress
class Command(BaseCommand):
    help = 'Send a message to "Sigmax" as a manual test.'

    def handle(self, *args, **options):
        self.stdout.write('Send a message to Sigmax.')
        msg = _generate_stuf_message({
            'signal_id': 'TEST MESSAGE FROM AMSTERDAM ' + str(uuid.uuid4())
        })

        self.stdout.write('Hier het bericht:')
        self.stdout.write(msg)
        self.stdout.write('Einde bericht')

        self.stdout.write('Sending a message to Sigmax.')
        r = _send_stuf_message(msg)
        self.stdout.write('response status code: {}'.format(r.status_code))
        self.stdout.write('Logging response.text :')
        self.stdout.write(r.text)
