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
        Register a handler under its callback identifier.

        :param callback_id: The callback identifier reported by the element.
        :type callback_id: str
        :param handler: The callable to invoke for that interaction.
        :type handler: Callable[..., Any]
        :return: None
        :rtype: None
        '''

        # Copy the current snapshot before adding the registration.
        handlers: Dict[str, Callable[..., Any]] = dict(self.handlers)
        handlers[callback_id] = handler

        # Apply the validated mapping update through the aggregate surface.
        self.set_attribute('handlers', handlers)

    # * method: freeze
    def freeze(self) -> CallbackTable:
        '''
        Freeze the working mapping into an independent callback-table snapshot.

        :return: The callback-table domain object for the render pass.
        :rtype: CallbackTable
        '''

        # Copy registrations so later aggregate changes cannot affect the snapshot.
        return CallbackTable(handlers=dict(self.handlers))
