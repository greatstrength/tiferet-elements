# *** imports

# ** app
from tiferet_elements.domain import CallbackTable

# *** functions

# ** function: button_handler
def button_handler(**kwargs):
    '''
    Return the callback parameters supplied by a button interaction.
    '''

    # Return the callback parameters unchanged.
    return kwargs

# *** tests

# ** test: test_callback_table_constructs_handler_mapping
def test_callback_table_constructs_handler_mapping():
    '''
    Construct a CallbackTable that maps a callback ID to a handler.
    '''

    # Construct a CallbackTable with a single button handler.
    callback_table = CallbackTable(handlers={'button_00': button_handler})

    # Verify the registered handler is the original callable.
    assert callback_table.handlers['button_00'] is button_handler
