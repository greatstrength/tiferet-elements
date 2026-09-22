"""Tiferet Elements Element Domain Tests"""

# *** imports

# ** core
from typing import Any

# ** app
from tiferet import use_tester
from tiferet_elements.domain import Element

# *** functions

# ** function: _normalize_element_tree
def _normalize_element_tree(value: Any) -> Any:
    '''
    Normalize nested Element instances or dict specs to comparable dicts.

    :param value: An Element, dict spec, or list of either.
    :type value: Any
    :return: A comparable nested dict or list of dicts.
    :rtype: Any
    '''

    # Normalize lists of nodes recursively.
    if isinstance(value, list):
        return [_normalize_element_tree(item) for item in value]

    # Normalize Element instances to a comparable mapping.
    if isinstance(value, Element):
        return {
            'type': value.type,
            'props': dict(value.props),
            'children': _normalize_element_tree(value.children),
        }

    # Normalize dict specs so omitted props/children match constructed defaults.
    if isinstance(value, dict):
        return {
            'type': value.get('type'),
            'props': dict(value.get('props') or {}),
            'children': _normalize_element_tree(value.get('children') or []),
        }

    # Return unrecognized values unchanged.
    return value

# *** testers

# ** tester: test_element
@use_tester(
    type='domain',
    target_cls=Element,
    sample_data={
        'type': 'Box',
        'props': {
            'sx': {
                'padding': 2,
            },
        },
        'children': [
            {
                'type': 'Button',
                'props': {
                    'variant': 'contained',
                },
            },
        ],
    },
    equality_fields=[
        'type',
        'props',
        'children',
    ],
    field_normalizers={
        'children': _normalize_element_tree,
    },
    description_cases=[],
)
class TestElement:
    '''
    Tests for Element.
    '''

    # * test: element_constructs_nested_children
    def test_element_constructs_nested_children(self, test_ctx) -> None:
        '''
        Test Element recursively constructs child domain objects.

        :param test_ctx: The bound domain tester context.
        :type test_ctx: object
        '''

        # Construct the nested widget description from sample data.
        element = test_ctx.make_target()

        # Assert construction against the nested sample tree.
        test_ctx.assert_new(element)
        test_ctx.assert_description(element)

        # Verify recursive child validation preserves the described tree.
        assert isinstance(element.children[0], Element)
        assert element.children[0].type == 'Button'
