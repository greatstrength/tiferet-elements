"""Tiferet Elements Mapper Test Configuration"""

# *** imports

# ** app
from tiferet.testing import register_mapper_hooks

# *** functions

# ** function: pytest_generate_tests
def pytest_generate_tests(metafunc):
    register_mapper_hooks(metafunc)
