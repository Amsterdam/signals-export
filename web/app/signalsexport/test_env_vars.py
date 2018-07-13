from unittest import mock
from django.test import TestCase
from signalsexport import env_vars


class CheckReqEnvVars(TestCase):
    # (not fully paramtrized, assumes SIGNALS,SIGMAX APIs for now)
    def should_fail(self):
        # missing credentials
        env_override = {
            'SIGNALS_USER': '',
            'SIGNALS_PASSWORD': '',
        }
        with mock.patch.dict('os.environ', env_override):
            success, mssg = env_vars.required_env_vars_are_present()
            self.assertEquals(success, False)

    def should_succeed(self):
        # all credentials present
        env_override = {
            'SIGNALS_USER': 'NOT EMPTY',
            'SIGNALS_PASSWORD': 'NOT EMPTY',
            'SIGMAX_AUTH_TOKEN': 'NOT EMPTY',
            'SIGMAX_SERVER': 'NOT EMPTY',
        }
        with mock.patch.dict('os.environ', env_override):
            success, mssg = env_vars.required_env_vars_are_present()
            self.assertEquals(success, True)
