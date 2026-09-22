"""Tiferet Elements Frame Domain Tests"""

# *** imports

# ** core
from typing import Any

# ** app
from tiferet import use_tester
from tiferet_elements.domain import Element, Frame

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

# ** tester: test_frame
@use_tester(
    type='domain',
    target_cls=Frame,
    sample_data={
        'elements': [
            {
                'type': 'Stack',
                'children': [
                    {
                        'type': 'TextField',
                    },
                ],
            },
        ],
    },
    equality_fields=[
        'elements',
    ],
    field_normalizers={
        'elements': _normalize_element_tree,
    },
    description_cases=[],
)
class TestFrame:
    '''
    Tests for Frame.
    '''

    # * test: frame_constructs_render_pass
    def test_frame_constructs_render_pass(self, test_ctx) -> None:
        '''
        Test Frame stores the root elements for one render pass.

        :param test_ctx: The bound domain tester context.
        :type test_ctx: object
        '''

        # Construct the frame from sample data.
        frame = test_ctx.make_target()

        # Assert construction against the nested sample tree.
        test_ctx.assert_new(frame)
        test_ctx.assert_description(frame)

        # Verify the composed tree remains available on the frame.
        assert len(frame.elements) == 1
        assert isinstance(frame.elements[0], Element)
        assert frame.elements[0].type == 'Stack'
        assert isinstance(frame.elements[0].children[0], Element)
        assert frame.elements[0].children[0].type == 'TextField'
