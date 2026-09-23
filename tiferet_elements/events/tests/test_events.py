"""Tiferet Elements Callback Event Tests."""

# *** imports

# ** infra
import pytest

# ** app
from tiferet.assets import TiferetError
from tiferet.testing import DomainEventTestBase
from tiferet_elements.assets import WIDGET_TYPE_NOT_FOUND_ID
from tiferet_elements.events import CreateElement

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
