"""Code-Declared DI Tests."""

# *** imports

# ** core
import ast
from pathlib import Path
from typing import Any

# ** infra
import pytest

# ** app
from tiferet.di.dependency_injector import DI_DEPENDENCY_NOT_REGISTERED_ID
from tiferet.domain import FlaggedDependency, ServiceRegistration
from tiferet.interfaces.core import ServiceError

from tiferet_elements.assets import STATE_SERVICE_ID
from tiferet_elements.di import DIContext
from tiferet_elements.interfaces import StateService
# *** classes

# ** class: stub_state_service
class StubStateService(StateService):
    '''Minimal StateService implementation used for dynamic DI resolution tests.'''

    # * method: get
    def get(self, key: str) -> Any:
        '''Return the requested key as a deterministic test value.

        :param key: The state value identifier.
        :type key: str
        :return: The requested key.
        :rtype: Any
        '''

        # Return the key as the deterministic stub response.
        return key

    # * method: set
    def set(self, key: str, value: Any) -> None:
        '''Accept a state value without persistence.

        :param key: The state value identifier.
        :type key: str
        :param value: The state value.
        :type value: Any
        '''

        # The stateless test stub has no value to persist.
        pass

# *** tests

# ** test: context_resolves_registered_dialect
def test_context_resolves_registered_dialect():
    '''Test that a code-declared registration resolves its matching dialect.'''

    # Build a registration that maps the Streamlit dialect to the local stand-in.
    registration = ServiceRegistration(
        id=STATE_SERVICE_ID,
        dependencies=[
            FlaggedDependency(
                flag='streamlit',
                module_path=__name__,
                class_name='StubStateService',
            ),
        ],
    )

    # Resolve the registered implementation through the MUI DI context.
    state_service = DIContext(
        service_configurations=[registration],
    ).get_dependency(STATE_SERVICE_ID, 'streamlit')

    # Verify the dialect-specific implementation was created.
    assert isinstance(state_service, StubStateService)

# ** test: context_rejects_unregistered_dialect
def test_context_rejects_unregistered_dialect():
    '''Test that an unregistered dialect produces Tiferet's clear DI error.'''

    # Define a registration only for the supported Streamlit dialect.
    registration = ServiceRegistration(
        id=STATE_SERVICE_ID,
        dependencies=[
            FlaggedDependency(
                flag='streamlit',
                module_path=__name__,
                class_name='StubStateService',
            ),
        ],
    )

    # Resolve an unknown dialect and verify its predictable DI failure.
    with pytest.raises(ServiceError) as error:
        DIContext(
            service_configurations=[registration],
        ).get_dependency(STATE_SERVICE_ID, 'unknown')

    # Verify the error identifies a missing dependency registration.
    assert error.value.error_code == DI_DEPENDENCY_NOT_REGISTERED_ID

# ** test: host_agnostic_modules_do_not_import_streamlit
def test_host_agnostic_modules_do_not_import_streamlit():
    '''Test that the interface, DI, and assets packages remain Streamlit-free.'''

    # Locate the package directories that must remain host agnostic.
    package_root = Path(__file__).parents[2]
    package_paths = [
        package_root / 'interfaces',
        package_root / 'di',
        package_root / 'assets',
    ]

    # Parse imports in every Python module and reject a Streamlit dependency.
    for package_path in package_paths:
        for module_path in package_path.rglob('*.py'):
            module = ast.parse(module_path.read_text())
            imports_streamlit = any(
                (
                    isinstance(node, ast.Import)
                    and any(alias.name == 'streamlit' for alias in node.names)
                )
                or (
                    isinstance(node, ast.ImportFrom)
                    and node.module is not None
                    and node.module.startswith('streamlit')
                )
                for node in ast.walk(module)
            )

            # Verify this host-agnostic module does not import Streamlit.
            assert not imports_streamlit, module_path
