"""Host-agnostic binding composition tests."""

# *** imports

# ** core
import subprocess
import sys
from pathlib import Path

# ** app
from tiferet_elements.blueprints.core import build_frame, build_handler_builder
from tiferet_elements.domain import Frame

# *** classes

# ** class: stub_state_service
class StubStateService:
    '''Provide deterministic reported state for composed handler tests.'''

    # * init
    def __init__(self, values: dict):
        '''
        Initialize the state service with its reported component values.

        :param values: The reported values keyed by component key.
        :type values: dict
        '''

        # Store the deterministic component values.
        self.values = values

    # * method: get
    def get(self, key):
        '''
        Return the reported value for one component key.

        :param key: The component key to retrieve.
        :type key: str
        :return: The reported value for the component.
        :rtype: Any
        '''

        # Return the stored value for the requested key.
        return self.values[key]

# ** class: stub_di_context
class StubDIContext:
    '''Record dependency requests while returning a deterministic state service.'''

    # * init
    def __init__(self, state_service):
        '''
        Initialize the resolver with its state-service result.

        :param state_service: The state service returned for each request.
        :type state_service: StubStateService
        '''

        # Store the state service returned by dependency resolution.
        self.state_service = state_service

        # Record each dependency request for assertions.
        self.requests = []

    # * method: get_dependency
    def get_dependency(self, service_id, dialect):
        '''
        Record a dependency lookup and return the configured state service.

        :param service_id: The requested service identifier.
        :type service_id: str
        :param dialect: The requested host dialect.
        :type dialect: str
        :return: The configured state service.
        :rtype: StubStateService
        '''

        # Record the requested service identifier and host dialect.
        self.requests.append((service_id, dialect))

        # Return the state service configured for this test.
        return self.state_service

# *** tests

# ** test: build_frame_materializes_widget_specs
def test_build_frame_materializes_widget_specs():
    '''
    Test that the public blueprint materializes recursive widget specifications.
    '''

    # Build the host-agnostic frame through the public composition entrypoint.
    frame = build_frame(
        elements=[
            {
                'widget_type': 'box',
                'children': [
                    {
                        'widget_type': 'button',
                        'props': {'children': 'Save'},
                    },
                ],
            },
        ],
    )

    # Verify the blueprint delegates to recursive domain-event composition.
    assert isinstance(frame, Frame)
    assert frame.elements[0].type == 'Box'
    assert frame.elements[0].children[0].type == 'Button'

# ** test: handler_builder_resolves_state_and_delivers_payload
def test_handler_builder_resolves_state_and_delivers_payload():
    '''
    Test that a composed handler resolves state and forwards its latest payload.
    '''

    # Compose the handler builder with deterministic reported component state.
    state_service = StubStateService(
        {'component': {'callback_00': {}}},
    )
    di_context = StubDIContext(state_service)
    received = []
    handler = build_handler_builder(
        dialect='test',
        di_context=di_context,
    )('component', received.append)

    # Invoke the zero-argument host handler to dispatch the latest state.
    handler()

    # Verify resolution occurs once and the callback receives the payload.
    assert di_context.requests == [('state_service', 'test')]
    assert received == [{'callback_00': {}}]

# ** test: core_import_does_not_require_streamlit
def test_core_import_does_not_require_streamlit():
    '''
    Test that host-agnostic blueprint imports do not require Streamlit.
    '''

    # Block every Streamlit import before importing the host-agnostic modules.
    script = '''
import builtins

original_import = builtins.__import__

def guarded_import(name, *args, **kwargs):
    if name == 'streamlit' or name.startswith('streamlit.'):
        raise ImportError('Streamlit import was attempted.')
    return original_import(name, *args, **kwargs)

builtins.__import__ = guarded_import

import tiferet_elements
import tiferet_elements.blueprints.core
'''

    # Run the guarded import check from the repository root.
    result = subprocess.run(
        [sys.executable, '-c', script],
        cwd=Path(__file__).parents[3],
        capture_output=True,
        text=True,
    )

    # Verify neither the package nor its core blueprint imports Streamlit.
    assert result.returncode == 0, result.stderr
