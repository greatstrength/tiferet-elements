# *** imports

# ** app
from tiferet.domain import ServiceRegistration

from ..assets import (
    STATE_SERVICE_ID,
    STATE_SERVICE_REGISTRATION_DATA,
)
from .core import DIContext

# *** constants

# ** constant: state_service_configuration
STATE_SERVICE_CONFIGURATION = ServiceRegistration(
    id=STATE_SERVICE_ID,
    **STATE_SERVICE_REGISTRATION_DATA,
)

# *** functions

# ** function: create_di_context
def create_di_context() -> DIContext:
    '''
    Create the default code-declared MUI dependency resolution context.

    :return: The MUI dependency resolution context.
    :rtype: DIContext
    '''

    # Build a context containing the prototype's state service registration.
    return DIContext(service_configurations=[STATE_SERVICE_CONFIGURATION])

# *** exports

__all__ = [
    'DIContext',
    'STATE_SERVICE_CONFIGURATION',
    'create_di_context',
]
