"""Tiferet Elements Callback Event Tests."""

# *** imports

# ** infra
import pytest

# ** app
from tiferet.assets import TiferetError
from tiferet.testing import DomainEventTestBase
from tiferet_elements.assets import (
    CALLBACK_NOT_FOUND_ID,
    WIDGET_TYPE_NOT_FOUND_ID,
)
from tiferet_elements.domain import CallbackTable, Frame
from tiferet_elements.events import (
    BuildCallbackTable,
    CreateElement,
    CreateFrame,
    DispatchCallback,
)
from tiferet_elements.mappers import CallbackTableAggregate, FrameAggregate
from conftest import button_handler, text_handler

# *** constants

# ** constant: frame
FRAME = Frame(
    elements=[
        {
            'type': 'Stack',
            'children': [
                {'type': 'Button', 'props': {'onClick': button_handler}},
                {'type': 'TextField', 'props': {'onChange': text_handler}},
            ],
        },
    ],
)

# ** constant: callback_table
CALLBACK_TABLE = CallbackTable(
    handlers={'button_00': button_handler},
)

# *** tests

# ** test: create_element
class TestCreateElement(DomainEventTestBase):
    '''Test Element materialization from registered widget defaults.'''

    # * attribute: event_cls
    event_cls = CreateElement

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {'widget_type': 'button'}

    # * attribute: required_params
    required_params = ['widget_type']

    # * test: merges_widget_defaults_props_and_children
    def test_merges_widget_defaults_props_and_children(self, mock_dependencies):
        '''
        Merge caller properties and preserve nested child Elements.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        '''

        # Create a Button with caller overrides and a nested TextField.
        element = self.handle(
            mock_dependencies,
            props={
                'children': 'Save',
                'color': 'primary',
                'variant': 'outlined',
            },
            children=[
                {
                    'type': 'TextField',
                    'props': {'label': 'Name'},
                },
            ],
        )

        # Verify the defaults, overrides, and recursive child were composed.
        assert element.type == 'Button'
        assert element.props == {
            'children': 'Save',
            'color': 'primary',
            'variant': 'outlined',
        }
        assert len(element.children) == 1
        assert element.children[0].type == 'TextField'
        assert element.children[0].props == {'label': 'Name'}

    # * test: materializes_new_widget_default_types
    @pytest.mark.parametrize(
        ('widget_type', 'element_type', 'default_props'),
        [
            ('icon', 'Icon', {}),
            ('card', 'Card', {'sx': {'p': 2}, 'variant': 'outlined'}),
            ('form_label', 'FormLabel', {}),
            ('typography', 'Typography', {'variant': 'h6'}),
        ],
    )
    def test_materializes_new_widget_default_types(
            self,
            mock_dependencies,
            widget_type,
            element_type,
            default_props,
        ):
        '''
        Materialize each newly catalogued widget type without overrides.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        :param widget_type: The catalog widget identifier.
        :type widget_type: str
        :param element_type: The expected Material UI element type.
        :type element_type: str
        :param default_props: The expected default properties.
        :type default_props: dict
        '''

        # Materialize the widget without caller-supplied properties.
        element = self.handle(
            mock_dependencies,
            widget_type=widget_type,
        )

        # Verify its catalogued element type and properties.
        assert element.type == element_type
        assert element.props == default_props

    # * test: raises_for_unrecognized_widget_type
    def test_raises_for_unrecognized_widget_type(self, mock_dependencies):
        '''
        Raise the widget-type error when no catalog entry exists.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        '''

        # Materialize an unknown widget and capture the structured error.
        with pytest.raises(TiferetError) as error:
            self.handle(
                mock_dependencies,
                widget_type='unknown',
            )

        # Verify the error code identifies the missing widget catalog entry.
        assert error.value.error_code == WIDGET_TYPE_NOT_FOUND_ID

# ** test: create_frame
class TestCreateFrame(DomainEventTestBase):
    '''Test recursive Frame materialization from widget specifications.'''

    # * attribute: event_cls
    event_cls = CreateFrame

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {
        'elements': [
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
    }

    # * attribute: required_params
    required_params = ['elements']

    # * test: builds_frozen_nested_frame
    def test_builds_frozen_nested_frame(self, mock_dependencies):
        '''
        Build an immutable Frame containing recursively materialized Elements.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        '''

        # Materialize the configured recursive widget specification.
        frame = self.handle(mock_dependencies)

        # Verify the event returns an immutable Frame instead of its aggregate.
        assert isinstance(frame, Frame)
        assert not isinstance(frame, FrameAggregate)

        # Verify the root Box defaults and nested Button override were composed.
        assert frame.elements[0].type == 'Box'
        assert frame.elements[0].props == {
            'component': 'div',
            'sx': {
                'border': '1px solid',
                'borderColor': 'divider',
                'borderRadius': 1,
                'p': 2,
            },
        }
        assert frame.elements[0].children[0].type == 'Button'
        assert frame.elements[0].children[0].props == {
            'children': 'Save',
            'variant': 'contained',
        }

    # * test: raises_for_unknown_nested_widget_type
    def test_raises_for_unknown_nested_widget_type(self, mock_dependencies):
        '''
        Propagate the catalog error from an unknown nested widget type.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        '''

        # Materialize a tree containing an unknown child widget specification.
        with pytest.raises(TiferetError) as error:
            self.handle(
                mock_dependencies,
                elements=[
                    {
                        'widget_type': 'box',
                        'children': [{'widget_type': 'unknown'}],
                    },
                ],
            )

        # Verify the delegated CreateElement error propagates unchanged.
        assert error.value.error_code == WIDGET_TYPE_NOT_FOUND_ID

# ** test: build_callback_table
class TestBuildCallbackTable(DomainEventTestBase):
    '''Test callback registration from interactive frame Elements.'''

    # * attribute: event_cls
    event_cls = BuildCallbackTable

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {'frame': FRAME}

    # * attribute: required_params
    required_params = ['frame']

    # * test: builds_frozen_table_with_distinct_callback_ids
    def test_builds_frozen_table_with_distinct_callback_ids(self, mock_dependencies):
        '''
        Build a frozen callback registry using distinct generated IDs.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        '''

        # Register each interactive child of the composed frame.
        callback_table = self.handle(mock_dependencies)
        button, text = FRAME.elements[0].children

        # Verify each callback received a distinct stable identifier.
        assert button.props['callback_id'] != text.props['callback_id']
        assert callback_table.handlers == {
            button.props['callback_id']: button_handler,
            text.props['callback_id']: text_handler,
        }

        # Verify registration returns an immutable domain snapshot.
        assert isinstance(callback_table, CallbackTable)
        assert not isinstance(callback_table, CallbackTableAggregate)
        with pytest.raises(AttributeError):
            callback_table.register('unexpected', button_handler)

# ** test: dispatch_callback
class TestDispatchCallback(DomainEventTestBase):
    '''Test callback lookup and handler dispatch from reported interactions.'''

    # * attribute: event_cls
    event_cls = DispatchCallback

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {
        'callback_table': CALLBACK_TABLE,
        'payload': {
            'button_00': {'value': 'clicked'},
            'timestamp': 1788552865158,
        },
    }

    # * attribute: required_params
    required_params = ['callback_table', 'payload']

    # * test: dispatches_registered_callback
    def test_dispatches_registered_callback(self, mock_dependencies):
        '''
        Dispatch a reported callback to its registered handler.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        '''

        # Dispatch the registered callback payload through the event.
        result = self.handle(mock_dependencies)

        # Verify the handler result preserves the reported parameters.
        assert result == {'value': 'clicked'}

    # * test: raises_for_unrecognized_callback_id
    def test_raises_for_unrecognized_callback_id(self, mock_dependencies):
        '''
        Raise the callback-not-found error for an unregistered identifier.

        :param mock_dependencies: The mocked event dependencies.
        :type mock_dependencies: dict
        '''

        # Dispatch an unknown callback and capture the structured error.
        with pytest.raises(TiferetError) as error:
            self.handle(
                mock_dependencies,
                payload={
                    'unknown_00': {},
                    'timestamp': 1788552865158,
                },
            )

        # Verify the error code identifies the unresolved callback.
        assert error.value.error_code == CALLBACK_NOT_FOUND_ID
