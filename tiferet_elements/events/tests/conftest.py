"""Tiferet Elements Event Test Hooks."""

# *** imports

# ** app
from tiferet.testing import register_event_hooks

# *** functions

# ** function: pytest_generate_tests
def pytest_generate_tests(metafunc):
    '''
    Register the Tiferet DomainEvent test harness parametrization.

    :param metafunc: The pytest test-generation metadata.
    :type metafunc: object
    '''

    # Register the required-parameter validation test cases.
    register_event_hooks(metafunc)
