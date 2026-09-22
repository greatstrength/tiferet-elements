# *** imports

# ** app
from tiferet.domain import ServiceRegistration
from ..assets import STATE_SERVICE_ID, STATE_SERVICE_REGISTRATION_DATA
from .core import ElementsServiceResolver

# *** constants

# ** constant: state_service_configuration
STATE_SERVICE_CONFIGURATION = ServiceRegistration(
    id=STATE_SERVICE_ID,
    **STATE_SERVICE_REGISTRATION_DATA,
)

# *** functions

# ** function: create_elements_service_resolver
def create_elements_service_resolver() -> ElementsServiceResolver:
    '''
    Create the default code-declared MUI ElementsServiceResolver.

    :return: The default MUI service resolver.
    :rtype: ElementsServiceResolver
    '''

    # Return the default MUI service resolver.
    return ElementsServiceResolver(
        service_configurations=[STATE_SERVICE_CONFIGURATION],
    )

# *** exports

__all__ = [
    'ElementsServiceResolver',
    'STATE_SERVICE_CONFIGURATION',
    'create_elements_service_resolver',
]
