"""Tiferet Elements Frame Mapper Tests"""

# *** imports

# ** app
from tiferet import use_tester
from tiferet_elements.domain import Element, Frame
from tiferet_elements.mappers import FrameAggregate, FrameTransferObject

# *** functions

# ** function: element_tree
def ELEMENT_TREE(element):
    '''
    Normalize an element dict or model into a comparable recursive tuple.

    :param element: The element data or domain object.
    :type element: dict | object
    :return: The normalized recursive element tuple.
    :rtype: tuple
    '''

    # Normalize serialized element data.
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

# ** constant: frame_sample_data
FRAME_SAMPLE_DATA = {
    'elements': [
        {
            'type': 'Stack',
            'props': {'spacing': 2},
            'children': [
                {
                    'type': 'TextField',
                    'props': {'label': 'Name'},
                    'children': [],
                },
            ],
        },
    ],
}

# ** constant: equality_fields
EQUALITY_FIELDS = [
    'elements',
]

# ** constant: field_normalizers
FIELD_NORMALIZERS = {
    'elements': lambda elements: tuple(ELEMENT_TREE(element) for element in elements),
}

# *** testers

# ** tester: test_frame_aggregate
@use_tester(
    type='aggregate',
    target_cls=FrameAggregate,
    sample_data=FRAME_SAMPLE_DATA,
    equality_fields=EQUALITY_FIELDS,
    field_normalizers=FIELD_NORMALIZERS,
    set_attribute_params=[
        ('elements', [], None),
        ('unknown', 'value', 'INVALID_MODEL_ATTRIBUTE'),
    ],
)
class TestFrameAggregate:
    '''
    Tests mutable Frame composition through the aggregate tester.
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

    # * test: add_element
    def test_add_element(self, test_ctx) -> None:
        '''
        Test add_element appends a validated root Element.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Construct a working Frame aggregate from sample data.
        aggregate = test_ctx.make_target()

        # Add one independently composed root Element.
        aggregate.add_element(Element(type='Button'))

        # Verify the aggregate retains both the original and added Elements.
        assert [element.type for element in aggregate.elements] == ['Stack', 'Button']

    # * test: freeze
    def test_freeze(self, test_ctx) -> None:
        '''
        Test freeze returns a Frame independent of later aggregate additions.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Construct a working Frame aggregate from sample data.
        aggregate = test_ctx.make_target()

        # Freeze the initial Frame composition.
        frozen = aggregate.freeze()

        # Add another Element after creating the snapshot.
        aggregate.add_element(Element(type='Button'))

        # Verify the frozen domain Frame retains its initial root tree.
        assert isinstance(frozen, Frame)
        assert not isinstance(frozen, FrameAggregate)
        assert [element.type for element in frozen.elements] == ['Stack']

# ** tester: test_frame_transfer_object
@use_tester(
    type='transfer_object',
    target_cls=FrameTransferObject,
    aggregate_cls=Frame,
    sample_data=FRAME_SAMPLE_DATA,
    aggregate_sample_data=FRAME_SAMPLE_DATA,
    equality_fields=EQUALITY_FIELDS,
    field_normalizers=FIELD_NORMALIZERS,
)
class TestFrameTransferObject:
    '''
    Tests frame mapping and JSON-safe recursive serialization through the transfer-object tester.
    '''

    # * test: map
    def test_map(self, test_ctx) -> None:
        '''
        Test TransferObject.map produces a Frame matching aggregate sample data.

        :param test_ctx: The bound transfer-object tester context.
        :type test_ctx: TransferObjectTesterContext
        '''

        # Assert mapping from serialized sample data.
        test_ctx.assert_map()

    # * test: from_model
    def test_from_model(self, test_ctx) -> None:
        '''
        Test TransferObject.from_model accepts the composed Frame.

        :param test_ctx: The bound transfer-object tester context.
        :type test_ctx: TransferObjectTesterContext
        '''

        # Assert from_model conversion from the aggregate sample.
        test_ctx.assert_from_model()

    # * test: round_trip
    def test_round_trip(self, test_ctx) -> None:
        '''
        Test Frame round-trips through the transfer object.

        :param test_ctx: The bound transfer-object tester context.
        :type test_ctx: TransferObjectTesterContext
        '''

        # Assert from_model then map preserves aggregate sample data.
        test_ctx.assert_round_trip()

    # * test: to_data
    def test_to_data(self) -> None:
        '''
        Test the frontend role emits the expected JSON-compatible props tree.
        '''

        # Construct a transfer object from the composed tree data.
        transfer_object = FrameTransferObject.model_validate(FRAME_SAMPLE_DATA)

        # Verify the frontend serialization retains only JSON-compatible tree data.
        assert transfer_object.to_primitive(role='to_data') == FRAME_SAMPLE_DATA
