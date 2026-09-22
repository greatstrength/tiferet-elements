"""Tiferet Elements Callback Table Mapper Tests"""

# *** imports

# ** app
from tiferet.testing import AggregateTestBase
from tiferet_elements.domain import CallbackTable
from tiferet_elements.mappers import CallbackTableAggregate
from tiferet_elements.mappers.tests.conftest import primary_handler, secondary_handler

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

# ** test: callback_table_aggregate
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
        ('handlers', {'text_01': secondary_handler}, None),
        ('unknown', 'value', 'INVALID_MODEL_ATTRIBUTE'),
    ]

    # * method: test_register
    def test_register(self, aggregate):
        '''
        Register a second callback handler.

        :param aggregate: The aggregate fixture under test.
        :type aggregate: CallbackTableAggregate
        '''

        # Register a second callback handler under its callback identifier.
        aggregate.register('text_01', secondary_handler)

        # Verify both handlers remain registered.
        assert aggregate.handlers == {
            'button_00': primary_handler,
            'text_01': secondary_handler,
        }

    # * method: test_freeze
    def test_freeze(self, aggregate):
        '''
        Freeze callback registrations before a later mutation.

        :param aggregate: The aggregate fixture under test.
        :type aggregate: CallbackTableAggregate
        '''

        # Freeze the initial registrations before registering another handler.
        frozen = aggregate.freeze()
        aggregate.register('text_01', secondary_handler)

        # Verify the frozen snapshot retains only the original registration.
        assert isinstance(frozen, CallbackTable)
        assert frozen.handlers == {'button_00': primary_handler}
