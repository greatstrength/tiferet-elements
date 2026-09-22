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
    'children': [{'type': 'Button', 'props': {'children': 'Save'}}],
}

# ** constant: equality_fields
EQUALITY_FIELDS = [
    'type',
    'props',
    'children',
]

# *** functions

# ** function: element_tree
def ELEMENT_TREE(element):
    '''
    Normalize a nested Element or element dict into a comparable tree.

    :param element: The Element model or equivalent dictionary.
    :type element: Element | dict
    :return: The comparable recursive element tuple.
    :rtype: tuple
    '''

    # Read the element values from either its model or serialized dictionary.
    if isinstance(element, dict):
        type = element['type']
        props = element.get('props', {})
        children = element.get('children', [])
    else:
        type = element.type
        props = element.props
        children = element.children

    # Normalize each child into the same recursive shape.
    return type, props, tuple(ELEMENT_TREE(child) for child in children)

# ** constant: field_normalizers
FIELD_NORMALIZERS = {
    'children': lambda children: tuple(ELEMENT_TREE(child) for child in children),
}

# *** tests

# ** test: element_aggregate
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
        Set each mutable Element attribute through its mapper methods.

        :param aggregate: The aggregate fixture under test.
        :type aggregate: ElementAggregate
        '''

        # Set each mutable element field through its dedicated operation.
        aggregate.set_type('Stack')
        aggregate.set_props({'spacing': 2})
        aggregate.set_children([])

        # Verify each field reflects its validated update.
        assert aggregate.type == 'Stack'
        assert aggregate.props == {'spacing': 2}
        assert aggregate.children == []

    # * method: test_freeze
    def test_freeze(self, aggregate):
        '''
        Freeze an Element aggregate before a later mutation.

        :param aggregate: The aggregate fixture under test.
        :type aggregate: ElementAggregate
        '''

        # Freeze the initial composition before changing its properties.
        frozen = aggregate.freeze()
        aggregate.set_props({'component': 'article'})

        # Verify the frozen snapshot remains a separate domain model.
        assert isinstance(frozen, Element)
        assert not isinstance(frozen, ElementAggregate)
        assert frozen.props == {'component': 'section'}
