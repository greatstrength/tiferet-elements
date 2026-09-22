"""Tiferet Elements State Interface."""

# *** imports

# ** core
from abc import abstractmethod
from typing import Any

# ** app
from tiferet.interfaces.core import Service

# *** interfaces

# ** interface: state_service
class StateService(Service):
    '''
    A host-agnostic session state contract that lets MUI interactions share
    values without coupling callers to a particular UI runtime.
    '''

    # * method: get
    @abstractmethod
    def get(self, key: str) -> Any:
        '''
        Retrieve a state value by key.

        Concrete hosts define their own unset-key behavior until the domain
        establishes a shared policy.

        :param key: The state key.
        :type key: str
        :return: The stored value.
        :rtype: Any
        '''
        raise NotImplementedError()

    # * method: set
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        '''
        Store a state value by key.

        :param key: The state key.
        :type key: str
        :param value: The value to store.
        :type value: Any
        :return: None
        :rtype: None
        '''
        raise NotImplementedError()
