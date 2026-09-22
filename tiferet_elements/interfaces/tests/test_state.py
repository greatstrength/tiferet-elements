"""StateService Interface Tests."""

# *** imports

# ** core
from typing import Any

# ** infra
import pytest

# ** app
from tiferet import use_tester
from tiferet_elements.interfaces import StateService

# *** classes

# ** class: memory_state
class MemoryState(StateService):
    '''Minimal host-neutral StateService used to exercise the interface contract.'''

    # * init
    def __init__(self) -> None:
        '''Initialize an empty in-memory state mapping.'''

        # Store values in a host-neutral mapping.
        self.values = {}

    # * method: get
    def get(self, key: str) -> Any:
        '''Return the stored state value for a key.

        :param key: The state value identifier.
        :type key: str
        :return: The stored state value.
        :rtype: Any
        '''

        # Return the stored value when present.
        return self.values.get(key)

    # * method: set
    def set(self, key: str, value: Any) -> None:
        '''Store a state value by key.

        :param key: The state value identifier.
        :type key: str
        :param value: The state value.
        :type value: Any
        '''

        # Persist the value in the in-memory mapping.
        self.values[key] = value

# *** testers

# ** tester: test_state_service
@use_tester(
    type='generic',
    target_cls=StateService,
)
class TestStateService:
    '''
    Tests for the StateService abstract contract.
    '''

    # * test: state_service_cannot_be_instantiated
    def test_state_service_cannot_be_instantiated(self, test_ctx) -> None:
        '''
        Test that StateService remains an abstract interface.

        :param test_ctx: The bound generic tester context.
        :type test_ctx: object
        '''

        # Resolve the abstract contract without instantiating it.
        target = test_ctx.make_target()

        # Lock the abstract method names on the interface.
        test_ctx.assert_contract(target)

        # Verify the abstract contract cannot be constructed directly.
        with pytest.raises(TypeError):
            target()

# ** tester: test_memory_state
@use_tester(
    type='generic',
    target_cls=MemoryState,
)
class TestMemoryState:
    '''
    Tests for a minimal concrete StateService.
    '''

    # * test: concrete_state_service_satisfies_contract
    def test_concrete_state_service_satisfies_contract(self, test_ctx) -> None:
        '''
        Test that a minimal concrete StateService can store and retrieve values.

        :param test_ctx: The bound generic tester context.
        :type test_ctx: object
        '''

        # Construct the in-memory implementation from sample data.
        state = test_ctx.make_target()

        # Store and retrieve a state value through the abstract contract.
        state.set('selection', 'item-1')

        # Verify the implementation satisfies both required methods.
        assert state.get('selection') == 'item-1'
