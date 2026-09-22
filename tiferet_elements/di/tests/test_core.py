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
    '''
    Provide a deterministic StateService implementation for DI resolution tests.
    '''

    # * method: get
    def get(self, key: str) -> Any:
        '''
        Return the requested key as a deterministic test value.

        :param key: The requested state key.
        :type key: str
        :return: The requested state key.
        :rtype: Any
        '''

        # Return the key to make successful construction observable.
        return key

    # * method: set
    def set(self, key: str, value: Any) -> None:
        '''
        Accept a state update without retaining it.

        :param key: The state key to update.
        :type key: str
        :param value: The state value to store.
        :type value: Any
        :return: None
        :rtype: None
        '''

        # The resolution stub deliberately has no mutable state.
        pass

# *** tests

# ** test: context_resolves_registered_dialect
def test_context_resolves_registered_dialect():
    '''
    Test that a context resolves the service registered for its host dialect.
    '''

    # Register the test-local StateService implementation for Streamlit.
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

    # Resolve the dependency for its registered dialect.
    state_service = DIContext(
        service_configurations=[registration],
    ).get_dependency(STATE_SERVICE_ID, 'streamlit')

    # Verify the resolved service uses the registered implementation.
    assert isinstance(state_service, StubStateService)

# ** test: context_rejects_unregistered_dialect
def test_context_rejects_unregistered_dialect():
    '''
    Test that a context reports an unregistered host dialect as a service error.
    '''

    # Register the test-local StateService implementation only for Streamlit.
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

    # Resolve an unknown dialect and verify the missing registration error.
    with pytest.raises(ServiceError) as error:
        DIContext(
            service_configurations=[registration],
        ).get_dependency(STATE_SERVICE_ID, 'unknown')

    assert error.value.error_code == DI_DEPENDENCY_NOT_REGISTERED_ID

# ** test: host_agnostic_modules_do_not_import_streamlit
def test_host_agnostic_modules_do_not_import_streamlit():
    '''
    Test that host-agnostic package modules do not import Streamlit directly.
    '''

    # Locate each host-agnostic package path subject to the import boundary.
    package_root = Path(__file__).parents[2]
    package_paths = [
        package_root / 'interfaces',
        package_root / 'di',
        package_root / 'assets',
    ]

    # Verify every Python module omits direct Streamlit imports.
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

            assert not imports_streamlit, module_path
