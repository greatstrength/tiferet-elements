"""Tiferet Elements Event Test Hooks."""

# *** imports

# ** app
from tiferet.testing import register_event_hooks

# *** functions

# ** function: pytest_generate_tests
def pytest_generate_tests(metafunc):
    register_event_hooks(metafunc)
