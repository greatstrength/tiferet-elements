"""Tiferet Elements Element Mapper Tests."""

# *** imports

# ** app
from tiferet.testing import AggregateTestBase

from tiferet_elements.domain import Element
from tiferet_elements.mappers import ElementAggregate

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

# ** constant: element_tree
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

# ** constant: field_normalizers
FIELD_NORMALIZERS = {
    'children': lambda children: tuple(ELEMENT_TREE(child) for child in children),
}

# *** tests

# ** test: TestElementAggregate
class TestElementAggregate(AggregateTestBase):
    '''
    Tests mutable Element composition through the mapper test harness.
    '''

    # * attribute: aggregate_cls
    aggregate_cls = ElementAggregate

    # * attribute: sample_data
    sample_data = ELEMENT_SAMPLE_DATA

    # * attribute: equality_fields
    equality_fields = EQUALITY_FIELDS

    # * attribute: field_normalizers
    field_normalizers = FIELD_NORMALIZERS

    # * attribute: set_attribute_params
    set_attribute_params = [
        ('type', 'Stack', None),
        ('props', {'spacing': 2}, None),
        ('children', [], None),
        ('unknown', 'value', 'INVALID_MODEL_ATTRIBUTE'),
    ]

    # * method: test_set_element_attributes
    def test_set_element_attributes(self, aggregate):
        '''
        Test the dedicated mutation methods delegate through set_attribute.

        :param aggregate: The harness-created Element aggregate.
        :type aggregate: ElementAggregate
        '''

        # Mutate each Element field through its aggregate surface.
        aggregate.set_type('Stack')
        aggregate.set_props({'spacing': 2})
        aggregate.set_children([])

        # Verify each validated mutation is reflected on the aggregate.
        assert aggregate.type == 'Stack'
        assert aggregate.props == {'spacing': 2}
        assert aggregate.children == []

    # * method: test_freeze
    def test_freeze(self, aggregate):
        '''
        Test freeze returns an Element independent of later aggregate mutation.

        :param aggregate: The harness-created Element aggregate.
        :type aggregate: ElementAggregate
        '''

        # Freeze the initial Element composition.
        frozen = aggregate.freeze()

        # Mutate the aggregate after its snapshot was created.
        aggregate.set_props({'component': 'article'})

        # Verify the frozen domain object retains its initial properties.
        assert isinstance(frozen, Element)
        assert not isinstance(frozen, ElementAggregate)
        assert frozen.props == {'component': 'section'}
