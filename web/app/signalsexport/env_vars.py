"""
Check that env vars for external projects are set.

Signals-export can be configured to talk to several external APIs/services,
some of whose settings and credentials must be present as environment
variables. This module can check that given a certain configuration all the
required environment variables are present. (Where the configuration is
a list of active services, that itself is set as an environment variable
ACTIVE_EXTERNAL_APIS.)
"""
import os
import logging
from django.conf import settings

# -- setup logging --
LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# For each supported API, credentials (or other settings from environment
# variables) should be added to this dictionary.
API_TO_ENV_VAR = {
    'SIGMAX': [
        'SIGMAX_AUTH_TOKEN',
        'SIGMAX_SERVER'
    ],
    'SIGNALS': [
        'SIGNALS_USER',
        'SIGNALS_PASSWORD'
    ]
}


def required_env_vars_are_present():
    """
    Check required environment variables are set for configured services.

    Note:
    * environment variables with an empty string value are considered not set.
    * returns True if all required variables are present, else False
    """
    error_msg = 'Environment variable {} must be set for service {}'
    n_errors = 0

    for api, variables in API_TO_ENV_VAR.items():
        if api not in settings.ACTIVE_EXTERNAL_APIS:
            continue

        for env_var in variables:
            if not os.getenv(env_var, None):
                logger.error(error_msg.format(env_var, api))
                n_errors += 1

    return False if n_errors else True
