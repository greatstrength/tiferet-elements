"""Tiferet Elements Callback Table Domain Tests"""

# *** imports

# ** app
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

# *** tests

# ** test: test_callback_table_constructs_handler_mapping
def test_callback_table_constructs_handler_mapping():
    '''
    Test CallbackTable stores the single-ID handler lookup shape.
    '''

    # Construct the callback-ID-to-handler snapshot.
    callback_table = CallbackTable(
        handlers={'button_00': button_handler},
    )

    # Verify the reported callback ID resolves to its callable handler.
    assert callback_table.handlers['button_00'] is button_handler
