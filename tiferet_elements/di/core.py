"""Tiferet Elements Code-Declared Dependency Injection."""

# *** imports

# ** core
from typing import List

# ** app
from tiferet.di import DIDynamicServiceContainer, ServiceResolver
from tiferet.domain import ServiceRegistration

# *** di

# ** di: elements_service_resolver
class ElementsServiceResolver(ServiceResolver):
    '''
    ElementsServiceResolver resolves MUI service registrations by host dialect
    without a configuration repository, keeping prototype composition explicit
    and portable.
    '''

    # * attribute: service_configurations
    service_configurations: List[ServiceRegistration]

    # * init
    def __init__(self, service_configurations: List[ServiceRegistration]) -> None:
        '''
        Initialize the resolver with its code-declared service registrations.

        :param service_configurations: The available MUI service registrations.
        :type service_configurations: List[ServiceRegistration]
        '''

        # Initialize the per-flag service container cache.
        super().__init__()

        # Store the service registrations for dialect-specific resolution.
        self.service_configurations = service_configurations

    # * method: build_container
    def build_container(self, flags: List[str]) -> DIDynamicServiceContainer:
        '''
        Build a dynamic container for the supplied host dialect flags.

        Registrations without a matching flagged dependency are deliberately
        omitted, allowing the inherited container to raise a clear
        ``ServiceError`` on resolution.

        :param flags: The normalized host dialect flags.
        :type flags: List[str]
        :return: The dynamic container for the supplied host dialect flags.
        :rtype: DIDynamicServiceContainer
        '''

        # Resolve each registration for the requested host dialect.
        services = {}
        for registration in self.service_configurations:
            dependency = registration.resolve_service(*flags)
            if dependency is not None:
                services[registration.id] = dependency

        # Return a container containing only the resolved registrations.
        return DIDynamicServiceContainer(services=services)
