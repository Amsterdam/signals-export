"""
Signal routing and base class for external API handlers.

Assumptions:
1) Each signal will be sent to 1 API at most (underlies both table design and
   routing implementation).
2) Each API handler catches any errors raised/caused by an external API in its
   handle method and returns a tuple of a Boolean False and a string description
   of the error if any.
"""
import logging
from collections import OrderedDict

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -- Keep the available handlers organized using a module global --
_HANDLERS = OrderedDict()  # we want to keep the order of registration


class BaseAPIHandler():
    name = None

    def handle(self, signal):
        """
        Given a signal call out to an external API.
        """
        # Expected return value a tuple of (success, status)
        # Make sure that any Exceptions caused by the interactions with external
        # APIs are silenced.
        raise NotImplementedError(
            'Subclass {} to provide an implementation.'.format(self.__class__))

    def can_handle(self, signal):
        """
        Check whether a signal is relevant to this external API.
        """
        raise NotImplementedError(
            'Subclass {} to provide an implementation.'.format(self.__class__))


def register_handler(handler):
    """
    Register an API handler (using the class info object, not an actual instance).

    Note: API handlers that are registered later take presedence.
    """
    h = handler()

    if not isinstance(h, BaseAPIHandler):
        logger.error('API handler must subclass {}'.format(BaseAPIHandler.__class__))
        raise TypeError

    if h.name is None:
        logging.error('API handler must have a name attribute.')
        raise ValueError

    if type(h.name) != type(''):
        logging.error('API handler name must be a string.')
        raise ValueError

    _HANDLERS[h.name] = h


def reset_handlers():
    """
    Reset the registered API handlers to intial state (only that LogOnlyHandler).
    """
    global _HANDLERS

    _HANDLERS = OrderedDict()
    register_handler(LogOnlyHandler)


def get_handler(signal):
    """
    Choose the correct API handler for a signal.
    """
    for handler in reversed(_HANDLERS.values()):
        if handler.can_handle(signal):
            return handler


# -- Initialize the available API handlers list with a default handler that only logs --

class LogOnlyHandler(BaseAPIHandler):
    """
    Handler that can handle any signal by just logging it.
    """
    name = 'local-log-only'

    def handle(self, signal):
        logger.info('Signal {} will only be logged'.format(signal['signal_id']))
        return True, 'Only logged'

    def can_handle(self, signal):
        return True

register_handler(LogOnlyHandler)  # make sure we always
