"""Tiferet Elements Mapper Test Configuration"""

# *** imports

# ** app
from tiferet.testing import register_mapper_hooks

# *** functions

# ** function: pytest_generate_tests
def pytest_generate_tests(metafunc):
    '''
    Register shared mapper-harness parametrization.

    :param metafunc: The pytest metafunc object.
    :type metafunc: object
    '''

    # Register mapper test parametrization.
    register_mapper_hooks(metafunc)
