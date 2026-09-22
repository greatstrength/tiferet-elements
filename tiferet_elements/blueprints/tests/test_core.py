"""Host-agnostic binding composition tests."""

# *** imports

# ** core
import subprocess
import sys
from pathlib import Path

# ** app
from tiferet import use_tester
from tiferet_elements.blueprints.core import build_frame, build_handler_builder
from tiferet_elements.domain import Frame

# *** classes

# ** class: stub_state_service
class StubStateService:
    '''Provide deterministic state reads for callback-builder tests.'''

    # * init
    def __init__(self, values):
        '''Initialize the state service from fixed values.

        :param values: The key-to-value mapping returned by get.
        :type values: dict
        '''

        # Store the deterministic state values.
        self.values = values

    # * method: get
    def get(self, key):
        '''Return the value registered for a state key.

        :param key: The requested state key.
        :type key: str
        :return: The fixed state value.
        :rtype: object
        '''

        # Return the requested state value.
        return self.values[key]

# ** class: stub_di_context
class StubDIContext:
    '''Record dialect resolution and return a preconfigured state service.'''

    # * init
    def __init__(self, state_service):
        '''Initialize from a state service.

        :param state_service: The service returned for a matching lookup.
        :type state_service: StubStateService
        '''

        # Store the dependency supplied by the test.
        self.state_service = state_service
        self.requests = []

    # * method: get_dependency
    def get_dependency(self, service_id, dialect):
        '''Record and resolve a dependency request.

        :param service_id: The requested dependency identifier.
        :type service_id: str
        :param dialect: The requested dialect.
        :type dialect: str
        :return: The configured state service.
        :rtype: StubStateService
        '''

        # Record the request made by the composition helper.
        self.requests.append((service_id, dialect))

        # Return the configured dependency.
        return self.state_service

# *** tests

# ** test: test_core_import_does_not_require_streamlit
def test_core_import_does_not_require_streamlit():
    '''Test the agnostic package and core blueprint import without Streamlit.'''

    # Block every Streamlit import in a fresh Python interpreter.
    script = '''
import builtins
original_import = builtins.__import__

def blocked_import(name, *args, **kwargs):
    if name == "streamlit" or name.startswith("streamlit."):
        raise ImportError("Streamlit import was attempted.")
    return original_import(name, *args, **kwargs)

builtins.__import__ = blocked_import
import tiferet_elements
import tiferet_elements.blueprints.core
'''

    # Run the isolated import path through the active test interpreter.
    result = subprocess.run(
        [sys.executable, '-c', script],
        capture_output=True,
        check=False,
        cwd=Path(__file__).parents[3],
        text=True,
    )

    # Verify the optional Streamlit dependency was never requested.
    assert result.returncode == 0, result.stderr

# *** testers

# ** tester: test_build_frame
@use_tester(
    type='generic',
    target_cls=build_frame,
)
class TestBuildFrame:
    '''
    Tests for the public build_frame blueprint.
    '''

    # * test: build_frame_materializes_widget_specs
    def test_build_frame_materializes_widget_specs(self, session) -> None:
        '''
        Test the public blueprint delegates recursive widget construction.

        :param session: A fresh test session.
        :type session: object
        '''

        # Build one nested Frame from plain consumer-facing specification data.
        frame = session.given(
            elements=[
                {
                    'widget_type': 'box',
                    'children': [
                        {
                            'widget_type': 'button',
                            'props': {
                                'children': 'Save',
                            },
                        },
                    ],
                },
            ],
        ).run()

        # Verify the blueprint returns the materialized immutable Frame tree.
        assert isinstance(frame, Frame)
        assert frame.elements[0].type == 'Box'
        assert frame.elements[0].children[0].type == 'Button'

# ** tester: test_build_handler_builder
@use_tester(
    type='generic',
    target_cls=build_handler_builder,
)
class TestBuildHandlerBuilder:
    '''
    Tests for the public build_handler_builder composition helper.
    '''

    # * test: handler_builder_resolves_state_and_delivers_payload
    def test_handler_builder_resolves_state_and_delivers_payload(self, session) -> None:
        '''
        Test the core composition helper resolves state before building callbacks.

        :param session: A fresh test session.
        :type session: object
        '''

        # Supply a fake resolver whose state has the latest component report.
        state_service = StubStateService({'component': {'callback_00': {}}})
        di_context = StubDIContext(state_service)
        received = []

        # Build the handler-builder through the bound generic target.
        handler_builder = session.given(
            dialect='test',
            di_context=di_context,
        ).run()

        # Invoke a zero-argument callback using the resolved state service.
        handler = handler_builder('component', received.append)
        handler()

        # Verify the requested dialect and the retrieved payload reached the consumer.
        assert di_context.requests == [('state_service', 'test')]
        assert received == [{'callback_00': {}}]
