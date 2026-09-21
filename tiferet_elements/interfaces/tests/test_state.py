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
    '''Test that StateService remains an abstract interface.'''

    # Verify the abstract contract cannot be constructed directly.
    with pytest.raises(TypeError):
        StateService()

# ** test: concrete_state_service_satisfies_contract
def test_concrete_state_service_satisfies_contract():
    '''Test that a minimal concrete StateService can store and retrieve values.'''

    # Define a minimal host-neutral implementation for the interface contract.
    class MemoryState(StateService):
        def __init__(self) -> None:
            self.values = {}

        def get(self, key: str) -> Any:
            return self.values.get(key)

        def set(self, key: str, value: Any) -> None:
            self.values[key] = value

    # Store and retrieve a state value through the abstract contract.
    state = MemoryState()
    state.set('selection', 'item-1')

    # Verify the implementation satisfies both required methods.
    assert state.get('selection') == 'item-1'
