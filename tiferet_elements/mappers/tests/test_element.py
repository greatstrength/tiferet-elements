"""Tiferet Elements Element Mapper Tests."""

# *** imports

# ** app
from tiferet import use_tester

from tiferet_elements.domain import Element
from tiferet_elements.mappers import ElementAggregate

# *** functions

# ** function: element_tree
def ELEMENT_TREE(element):
    '''
    Normalize an element dict or model into a comparable recursive tuple.

    :param element: The Element data or domain object.
    :type element: dict | Element
    :return: The normalized recursive element tuple.
    :rtype: tuple
    '''

    # Normalize serialized Element data.
    if isinstance(element, dict):
        return (
            element['type'],
            element.get('props', {}),
            tuple(ELEMENT_TREE(child) for child in element.get('children', [])),
        )

    # Normalize an Element domain object.
    return (
        element.type,
        element.props,
        tuple(ELEMENT_TREE(child) for child in element.children),
    )

# *** constants

# ** constant: element_sample_data
ELEMENT_SAMPLE_DATA = {
    'type': 'Box',
    'props': {'component': 'section'},
    'children': [
        {
            'type': 'Button',
            'props': {'children': 'Save'},
        },
    ],
}

# ** constant: equality_fields
EQUALITY_FIELDS = [
    'type',
    'props',
    'children',
]

# ** constant: field_normalizers
FIELD_NORMALIZERS = {
    'children': lambda children: tuple(ELEMENT_TREE(child) for child in children),
}

# *** testers

# ** tester: test_element_aggregate
@use_tester(
    type='aggregate',
    target_cls=ElementAggregate,
    sample_data=ELEMENT_SAMPLE_DATA,
    equality_fields=EQUALITY_FIELDS,
    field_normalizers=FIELD_NORMALIZERS,
    set_attribute_params=[
        ('type', 'Stack', None),
        ('props', {'spacing': 2}, None),
        ('children', [], None),
        ('unknown', 'value', 'INVALID_MODEL_ATTRIBUTE'),
    ],
)
class TestElementAggregate:
    '''
    Tests mutable Element composition through the aggregate tester.
    '''

    # * test: new
    def test_new(self, test_ctx) -> None:
        '''
        Test aggregate instantiation matches sample data.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Assert construction against sample data.
        test_ctx.assert_new()

    # * test: set_attribute
    def test_set_attribute(self, test_ctx) -> None:
        '''
        Test set_attribute accepts valid fields and rejects unknown attributes.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Assert each configured set-attribute case.
        test_ctx.assert_set_attribute()

    # * test: set_element_attributes
    def test_set_element_attributes(self, test_ctx) -> None:
        '''
        Test the dedicated mutation methods delegate through set_attribute.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Construct a working Element aggregate from sample data.
        aggregate = test_ctx.make_target()

        # Mutate each Element field through its aggregate surface.
        aggregate.set_type('Stack')
        aggregate.set_props({'spacing': 2})
        aggregate.set_children([])

        # Verify each validated mutation is reflected on the aggregate.
        assert aggregate.type == 'Stack'
        assert aggregate.props == {'spacing': 2}
        assert aggregate.children == []

    # * test: freeze
    def test_freeze(self, test_ctx) -> None:
        '''
        Test freeze returns an Element independent of later aggregate mutation.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Construct a working Element aggregate from sample data.
        aggregate = test_ctx.make_target()

        # Freeze the initial Element composition.
        frozen = aggregate.freeze()

        # Mutate the aggregate after its snapshot was created.
        aggregate.set_props({'component': 'article'})

        # Verify the frozen domain object retains its initial properties.
        assert isinstance(frozen, Element)
        assert not isinstance(frozen, ElementAggregate)
        assert frozen.props == {'component': 'section'}
