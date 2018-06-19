# query signals API to find potentially sendable signals
# check local database for those messages that were not yet sent
# send the messages, and mark them as sent
"""
Download datasets from objectstore, save them in local directory.
"""
import os

from django.core.management.base import BaseCommand, CommandError

from datasets.handle_signals import handle_signals


class Command(BaseCommand):
    help = 'Retrieve signals from signal API and send messages if needed.'

    def handle(self, *args, **options):
        self.stdout.write('Not yet implemented')
        handle_signals()

