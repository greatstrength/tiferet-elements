"""Tiferet Elements Callback Table Domain Tests"""

# *** imports

# ** app
from tiferet import use_tester
from tiferet_elements.domain import CallbackTable

# *** functions

# ** function: button_handler
def button_handler(**kwargs):
    '''
    Return the callback parameters supplied by a button interaction.

    :param kwargs: The callback parameters.
    :type kwargs: dict
    :return: The supplied callback parameters.
    :rtype: dict
    '''

    # Return the supplied callback parameters.
    return kwargs

# *** testers

# ** tester: test_callback_table
@use_tester(
    type='domain',
    target_cls=CallbackTable,
    sample_data={
        'handlers': {
            'button_00': button_handler,
        },
    },
    equality_fields=[
        'handlers',
    ],
    description_cases=[],
)
class TestCallbackTable:
    '''
    Tests for CallbackTable.
    '''

    # * test: callback_table_constructs_handler_mapping
    def test_callback_table_constructs_handler_mapping(self, test_ctx) -> None:
        '''
        Test CallbackTable stores the single-ID handler lookup shape.

        :param test_ctx: The bound domain tester context.
        :type test_ctx: object
        '''

        # Construct the callback-ID-to-handler snapshot from sample data.
        callback_table = test_ctx.make_target()

        # Assert construction against the sample handler mapping.
        test_ctx.assert_new(callback_table)
        test_ctx.assert_description(callback_table)

        # Verify the reported callback ID resolves to its callable handler.
        assert callback_table.handlers['button_00'] is button_handler
