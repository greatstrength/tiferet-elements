"""StateService Interface Tests."""

# *** imports

# ** core
from typing import Any

# ** infra
import pytest

# ** app
from tiferet_elements.interfaces import StateService

# *** tests

# ** test: state_service_cannot_be_instantiated
def test_state_service_cannot_be_instantiated():
    '''
    Test that StateService cannot be constructed directly.
    '''

    # Assert the abstract contract cannot be instantiated.
    with pytest.raises(TypeError):
        StateService()

# ** test: concrete_state_service_satisfies_contract
def test_concrete_state_service_satisfies_contract():
    '''
    Test that a concrete subclass implementing get and set round-trips a value.
    '''

    # Define a minimal in-memory StateService implementation.
    class MemoryState(StateService):

        def __init__(self):
            self.values = {}

        def get(self, key: str) -> Any:
            return self.values.get(key)

        def set(self, key: str, value: Any) -> None:
            self.values[key] = value

    # Instantiate the concrete service and round-trip a stored value.
    state = MemoryState()
    state.set('selection', 'item-1')
    assert state.get('selection') == 'item-1'
