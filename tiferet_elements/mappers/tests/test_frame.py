"""Tiferet Elements Frame Mapper Tests"""

# *** imports

# ** app
from tiferet.testing import AggregateTestBase, TransferObjectTestBase
from tiferet_elements.domain import Element, Frame
from tiferet_elements.mappers import FrameAggregate, FrameTransferObject
from tiferet_elements.mappers.tests.conftest import element_tree

# *** constants

# ** constant: frame_sample_data
FRAME_SAMPLE_DATA = {
    'elements': [{
        'type': 'Stack',
        'props': {'spacing': 2},
        'children': [{
            'type': 'TextField',
            'props': {'label': 'Name'},
            'children': [],
        }],
    }],
}

# ** constant: equality_fields
EQUALITY_FIELDS = [
    'elements',
]

# ** constant: field_normalizers
FIELD_NORMALIZERS = {
    'elements': lambda elements: tuple(element_tree(element) for element in elements),
}

# *** tests

# ** test: frame_aggregate
class TestFrameAggregate(AggregateTestBase):
    '''
    Tests mutable Frame composition through the mapper test harness.
    '''

    # * attribute: aggregate_cls
    aggregate_cls = FrameAggregate

    # * attribute: sample_data
    sample_data = FRAME_SAMPLE_DATA

    # * attribute: equality_fields
    equality_fields = EQUALITY_FIELDS

    # * attribute: field_normalizers
    field_normalizers = FIELD_NORMALIZERS

    # * attribute: set_attribute_params
    set_attribute_params = [
        ('elements', [], None),
        ('unknown', 'value', 'INVALID_MODEL_ATTRIBUTE'),
    ]

    # * method: test_add_element
    def test_add_element(self, aggregate):
        '''
        Append an element to a composed Frame.

        :param aggregate: The aggregate fixture under test.
        :type aggregate: FrameAggregate
        '''

        # Add a second root element through the aggregate operation.
        aggregate.add_element(Element(type='Button'))

        # Verify the composition preserves both root elements.
        assert [element.type for element in aggregate.elements] == ['Stack', 'Button']

    # * method: test_freeze
    def test_freeze(self, aggregate):
        '''
        Freeze a Frame aggregate before a later mutation.

        :param aggregate: The aggregate fixture under test.
        :type aggregate: FrameAggregate
        '''

        # Freeze the initial composition before adding a second root element.
        frozen = aggregate.freeze()
        aggregate.add_element(Element(type='Button'))

        # Verify the frozen snapshot retains only the original root element.
        assert isinstance(frozen, Frame)
        assert not isinstance(frozen, FrameAggregate)
        assert [element.type for element in frozen.elements] == ['Stack']


# ** test: frame_transfer_object
class TestFrameTransferObject(TransferObjectTestBase):
    '''
    Tests frame mapping and JSON-safe recursive serialization through the harness.
    '''

    # * attribute: transfer_cls
    transfer_cls = FrameTransferObject

    # * attribute: aggregate_cls
    aggregate_cls = Frame

    # * attribute: sample_data
    sample_data = FRAME_SAMPLE_DATA

    # * attribute: aggregate_sample_data
    aggregate_sample_data = FRAME_SAMPLE_DATA

    # * attribute: equality_fields
    equality_fields = EQUALITY_FIELDS

    # * attribute: field_normalizers
    field_normalizers = FIELD_NORMALIZERS

    # * method: test_to_data
    def test_to_data(self):
        '''
        Serialize nested frame transfer data into a JSON-safe tree.
        '''

        # Construct transfer data from the recursive sample tree.
        transfer_object = FrameTransferObject.model_validate(FRAME_SAMPLE_DATA)

        # Verify JSON-mode serialization preserves the input tree.
        assert transfer_object.to_primitive(role='to_data') == FRAME_SAMPLE_DATA
