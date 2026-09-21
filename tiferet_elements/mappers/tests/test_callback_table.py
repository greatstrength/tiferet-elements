"""Tiferet Elements Callback Table Mapper Tests"""

# *** imports

# ** app
from tiferet.testing import AggregateTestBase
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

# *** tests

# ** test: TestCallbackTableAggregate
class TestCallbackTableAggregate(AggregateTestBase):
    '''
    Tests the mutable callback-registration aggregate through the mapper harness.
    '''

    # * attribute: aggregate_cls
    aggregate_cls = CallbackTableAggregate

    # * attribute: sample_data
    sample_data = CALLBACK_TABLE_SAMPLE_DATA

    # * attribute: equality_fields
    equality_fields = EQUALITY_FIELDS

    # * attribute: set_attribute_params
    set_attribute_params = [
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
    ]

    # * method: test_register
    def test_register(self, aggregate):
        '''
        Test register creates a validated callback-table entry.

        :param aggregate: The harness-created callback-table aggregate.
        :type aggregate: CallbackTableAggregate
        '''

        # Register a second callback handler.
        aggregate.register('text_01', secondary_handler)

        # Verify both callback IDs resolve to their handlers.
        assert aggregate.handlers == {
            'button_00': primary_handler,
            'text_01': secondary_handler,
        }

    # * method: test_freeze
    def test_freeze(self, aggregate):
        '''
        Test freeze returns an independent callback-table domain snapshot.

        :param aggregate: The harness-created callback-table aggregate.
        :type aggregate: CallbackTableAggregate
        '''

        # Freeze the initial registration state.
        frozen = aggregate.freeze()

        # Mutate the working aggregate after the snapshot was created.
        aggregate.register('text_01', secondary_handler)

        # Verify the frozen domain object is independent of later mutations.
        assert isinstance(frozen, CallbackTable)
        assert frozen.handlers == {'button_00': primary_handler}
