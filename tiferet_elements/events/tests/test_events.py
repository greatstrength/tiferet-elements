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

# *** functions

# ** function: button_handler
def button_handler(**kwargs):
    '''
    Return the parameters reported by a button interaction.

    :param kwargs: The callback parameters.
    :type kwargs: dict
    :return: The supplied callback parameters.
    :rtype: dict
    '''

    # Return the supplied callback parameters.
    return kwargs

# ** function: text_handler
def text_handler(**kwargs):
    '''
    Return the parameters reported by a text interaction.

    :param kwargs: The callback parameters.
    :type kwargs: dict
    :return: The supplied callback parameters.
    :rtype: dict
    '''

    # Return the supplied callback parameters.
    return kwargs

# *** constants

# ** constant: frame
FRAME = Frame(
    elements=[
        {
            'type': 'Stack',
            'children': [
                {
                    'type': 'Button',
                    'props': {'onClick': button_handler},
                },
                {
                    'type': 'TextField',
                    'props': {'onChange': text_handler},
                },
            ],
        },
    ],
)

# ** constant: callback_table
CALLBACK_TABLE = CallbackTable(
    handlers={'button_00': button_handler},
)

# *** tests

# ** test: TestCreateFrame
class TestCreateFrame(DomainEventTestBase):
    '''
    Tests recursive Frame construction through the DomainEvent test harness.
    '''

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

    # * method: test_builds_frozen_nested_frame
    def test_builds_frozen_nested_frame(self, mock_dependencies):
        '''
        Test recursive specifications produce a frozen Frame tree.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Build the recursive widget specifications through DomainEvent.handle.
        frame = self.handle(mock_dependencies)

        # Verify the event returns a frozen Frame with materialized descendants.
        assert isinstance(frame, Frame)
        assert not isinstance(frame, FrameAggregate)
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

    # * method: test_raises_for_unknown_nested_widget_type
    def test_raises_for_unknown_nested_widget_type(self, mock_dependencies):
        '''
        Test unknown widget types reuse CreateElement's catalogue error.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Build a tree that contains an unregistered child widget type.
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

        # Verify recursive construction exposes the shared unknown-widget error.
        assert error.value.error_code == WIDGET_TYPE_NOT_FOUND_ID

# ** test: TestCreateElement
class TestCreateElement(DomainEventTestBase):
    '''
    Tests Element construction through the DomainEvent test harness.
    '''

    # * attribute: event_cls
    event_cls = CreateElement

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {'widget_type': 'button'}

    # * attribute: required_params
    required_params = ['widget_type']

    # * method: test_merges_widget_defaults_props_and_children
    def test_merges_widget_defaults_props_and_children(self, mock_dependencies):
        '''
        Test the event combines defaults, MUI properties, and nested elements.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Create a Button with property overrides and one nested Element child.
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

        # Verify props override defaults without replacing Element children.
        assert element.type == 'Button'
        assert element.props == {
            'children': 'Save',
            'color': 'primary',
            'variant': 'outlined',
        }
        assert len(element.children) == 1
        assert element.children[0].type == 'TextField'
        assert element.children[0].props == {'label': 'Name'}

    # * method: test_materializes_new_widget_default_types
    @pytest.mark.parametrize(
        ('widget_type', 'element_type', 'default_props'),
        [
            ('icon', 'Icon', {}),
            (
                'card',
                'Card',
                {
                    'sx': {
                        'p': 2,
                    },
                    'variant': 'outlined',
                },
            ),
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
        Test each expanded catalog widget materializes its MUI element type.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        :param widget_type: The catalog key used to create the Element.
        :type widget_type: str
        :param element_type: The Material UI component type expected in the Element.
        :type element_type: str
        :param default_props: The default Material UI properties expected in the Element.
        :type default_props: dict
        '''

        # Materialize the widget through the public event test-harness path.
        element = self.handle(
            mock_dependencies,
            widget_type=widget_type,
        )

        # Verify the catalog defaults produce the confirmed type and properties.
        assert element.type == element_type
        assert element.props == default_props

    # * method: test_raises_for_unrecognized_widget_type
    def test_raises_for_unrecognized_widget_type(self, mock_dependencies):
        '''
        Test an unknown widget type raises the catalogued domain error.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Request a widget type without any registered default shape.
        with pytest.raises(TiferetError) as error:
            self.handle(
                mock_dependencies,
                widget_type='unknown',
            )

        # Verify the event surfaces the catalogue lookup error.
        assert error.value.error_code == WIDGET_TYPE_NOT_FOUND_ID

# ** test: TestBuildCallbackTable
class TestBuildCallbackTable(DomainEventTestBase):
    '''
    Tests callback-table construction through the DomainEvent test harness.
    '''

    # * attribute: event_cls
    event_cls = BuildCallbackTable

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {'frame': FRAME}

    # * attribute: required_params
    required_params = ['frame']

    # * method: test_builds_frozen_table_with_distinct_callback_ids
    def test_builds_frozen_table_with_distinct_callback_ids(self, mock_dependencies):
        '''
        Test a tree walk registers multiple handlers under distinct identifiers.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Build the callback table through DomainEvent.handle.
        callback_table = self.handle(mock_dependencies)

        # Verify every interactive element received a unique identifier.
        button, text = FRAME.elements[0].children
        assert button.props['callback_id'] != text.props['callback_id']
        assert callback_table.handlers == {
            button.props['callback_id']: button_handler,
            text.props['callback_id']: text_handler,
        }

        # Verify callers receive the frozen domain object, not the aggregate.
        assert isinstance(callback_table, CallbackTable)
        assert not isinstance(callback_table, CallbackTableAggregate)
        with pytest.raises(AttributeError):
            callback_table.register('unexpected', button_handler)

# ** test: TestDispatchCallback
class TestDispatchCallback(DomainEventTestBase):
    '''
    Tests callback dispatch through the DomainEvent test harness.
    '''

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

    # * method: test_dispatches_registered_callback
    def test_dispatches_registered_callback(self, mock_dependencies):
        '''
        Test the registered handler receives its payload-defined parameters.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Dispatch the confirmed composite payload through DomainEvent.handle.
        result = self.handle(mock_dependencies)

        # Verify the matching handler returned its interaction parameters.
        assert result == {'value': 'clicked'}

    # * method: test_raises_for_unrecognized_callback_id
    def test_raises_for_unrecognized_callback_id(self, mock_dependencies):
        '''
        Test an interaction without a registered handler is a domain error.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Dispatch an interaction whose callback ID was not registered.
        with pytest.raises(TiferetError) as error:
            self.handle(
                mock_dependencies,
                payload={
                    'unknown_00': {},
                    'timestamp': 1788552865158,
                },
            )

        # Verify dispatch reports the catalogued callback-not-found outcome.
        assert error.value.error_code == CALLBACK_NOT_FOUND_ID
