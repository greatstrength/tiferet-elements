"""Tiferet Elements Callback Table Mappers"""

# *** imports

# ** core
from typing import Any, Callable, Dict

# ** app
from tiferet.mappers import Aggregate
from ..domain import CallbackTable

# *** mappers

# ** mapper: callback_table_aggregate
class CallbackTableAggregate(CallbackTable, Aggregate):
    '''
    Provides the mutable registration surface used while a frame's callback
    snapshot is built before later dispatch reads its frozen domain form.
    '''

    # * method: register
    def register(self, callback_id: str, handler: Callable[..., Any]) -> None:
        '''
        Register a callback handler under its callback identifier.

        :param callback_id: The callback identifier used for later dispatch.
        :type callback_id: str
        :param handler: The callback handler to register.
        :type handler: Callable[..., Any]
        :return: None
        :rtype: None
        '''

        # Copy existing registrations before adding the new callback handler.
        handlers = dict(self.handlers)
        handlers[callback_id] = handler

        # Validate and store the extended handler mapping.
        self.set_attribute('handlers', handlers)

    # * method: freeze
    def freeze(self) -> CallbackTable:
        '''
        Freeze the current callback registrations into a domain snapshot.

        :return: The immutable CallbackTable snapshot.
        :rtype: CallbackTable
        '''

        # Copy the handler mapping into the immutable domain snapshot.
        return CallbackTable(handlers=dict(self.handlers))
