"""Tiferet Elements Code-Declared Dependency Injection."""

# *** imports

# ** core
from typing import List

# ** app
from tiferet.di import DIDynamicServiceContainer, ServiceResolver
from tiferet.domain import ServiceRegistration

# *** di

# ** di: context
class DIContext(ServiceResolver):
    '''
    Resolve MUI service registrations by host dialect without a configuration
    repository, keeping prototype composition explicit and portable.
    '''

    # * attribute: service_configurations
    service_configurations: List[ServiceRegistration]

    # * init
    def __init__(self, service_configurations: List[ServiceRegistration]) -> None:
        '''
        Initialize the resolver from code-declared service registrations.

        :param service_configurations: The host-specific service registrations.
        :type service_configurations: List[ServiceRegistration]
        '''

        # Initialize the per-flag container cache.
        super().__init__()

        # Store the code-declared service registrations.
        self.service_configurations = service_configurations

    # * method: build_container
    def build_container(self, flags: List[str]) -> DIDynamicServiceContainer:
        '''
        Build a dynamic service container for the requested host dialect flags.

        Registrations without a matching flagged dependency are deliberately
        omitted, allowing the inherited container to raise a clear ServiceError.

        :param flags: The normalized host dialect flags.
        :type flags: List[str]
        :return: A container with dependencies registered for the matching flags.
        :rtype: DIDynamicServiceContainer
        '''

        # Resolve each registration's effective dependency for the requested flags.
        services = {}
        for registration in self.service_configurations:
            dependency = registration.resolve_service(*flags)
            if dependency is not None:
                services[registration.id] = dependency

        # Build a factory-based container for the resolved host dependencies.
        return DIDynamicServiceContainer(services=services)
