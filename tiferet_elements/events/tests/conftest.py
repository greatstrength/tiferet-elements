"""Tiferet Elements Event Test Hooks."""

# *** imports

# ** app
from tiferet.testing import register_event_hooks

# *** functions

# ** function: pytest_generate_tests
def pytest_generate_tests(metafunc):
    register_event_hooks(metafunc)

# ** function: button_handler
def button_handler(**kwargs):
    '''
    Return the parameters reported by a button interaction.

    :param kwargs: The parameters reported by the host.
    :type kwargs: dict
    :return: The reported interaction parameters.
    :rtype: dict
    '''

    # Return the parameters supplied by the host interaction.
    return kwargs

# ** function: text_handler
def text_handler(**kwargs):
    '''
    Return the parameters reported by a text interaction.

    :param kwargs: The parameters reported by the host.
    :type kwargs: dict
    :return: The reported interaction parameters.
    :rtype: dict
    '''

    # Return the parameters supplied by the host interaction.
    return kwargs
