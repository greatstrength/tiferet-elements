"""Tiferet Elements Callback Table Mapper Tests"""

# *** imports

# ** app
from tiferet import use_tester
from tiferet_elements.domain import CallbackTable
from tiferet_elements.mappers import CallbackTableAggregate

# *** functions

# ** function: primary_handler
def primary_handler(**kwargs):
    '''
    Return the supplied primary callback parameters.

    :param kwargs: The callback parameters.
    :type kwargs: dict
    :return: The supplied callback parameters.
    :rtype: dict
    '''

    # Return the supplied callback parameters.
    return kwargs

# ** function: secondary_handler
def secondary_handler(**kwargs):
    '''
    Return the supplied secondary callback parameters.

    :param kwargs: The callback parameters.
    :type kwargs: dict
    :return: The supplied callback parameters.
    :rtype: dict
    '''

    # Return the supplied callback parameters.
    return kwargs

# *** constants

# ** constant: callback_table_sample_data
CALLBACK_TABLE_SAMPLE_DATA = {
    'handlers': {
        'button_00': primary_handler,
    },
}

# ** constant: equality_fields
EQUALITY_FIELDS = [
    'handlers',
]

# *** testers

# ** tester: test_callback_table_aggregate
@use_tester(
    type='aggregate',
    target_cls=CallbackTableAggregate,
    sample_data=CALLBACK_TABLE_SAMPLE_DATA,
    equality_fields=EQUALITY_FIELDS,
    set_attribute_params=[
        (
            'handlers',
            {'text_01': secondary_handler},
            None,
        ),
        (
            'unknown',
            'value',
            'INVALID_MODEL_ATTRIBUTE',
        ),
    ],
)
class TestCallbackTableAggregate:
    '''
    Tests the mutable callback-registration aggregate through the aggregate tester.
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

    # * test: register
    def test_register(self, test_ctx) -> None:
        '''
        Test register creates a validated callback-table entry.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Construct a working callback-table aggregate from sample data.
        aggregate = test_ctx.make_target()

        # Register a second callback handler.
        aggregate.register('text_01', secondary_handler)

        # Verify both callback IDs resolve to their handlers.
        assert aggregate.handlers == {
            'button_00': primary_handler,
            'text_01': secondary_handler,
        }

    # * test: freeze
    def test_freeze(self, test_ctx) -> None:
        '''
        Test freeze returns an independent callback-table domain snapshot.

        :param test_ctx: The bound aggregate tester context.
        :type test_ctx: AggregateTesterContext
        '''

        # Construct a working callback-table aggregate from sample data.
        aggregate = test_ctx.make_target()

        # Freeze the initial registration state.
        frozen = aggregate.freeze()

        # Mutate the working aggregate after the snapshot was created.
        aggregate.register('text_01', secondary_handler)

        # Verify the frozen domain object is independent of later mutations.
        assert isinstance(frozen, CallbackTable)
        assert frozen.handlers == {'button_00': primary_handler}
