"""Host-agnostic binding composition for Tiferet Elements."""

from __future__ import annotations

# *** imports

# ** core
from typing import TYPE_CHECKING, Any, Callable

# ** app
from tiferet.events import DomainEvent
from ..assets import STATE_SERVICE_ID
from ..di import create_di_context
from ..events import CreateFrame

if TYPE_CHECKING:
    from ..domain import Frame

# *** functions

# ** function: build_handler_builder
def build_handler_builder(
        dialect: str = 'streamlit',
        di_context: Any = None,
    ) -> Callable[[str, Callable[[Any], Any]], Callable[[], Any]]:
    '''
    Build state-backed no-argument host callback handlers for one dialect.

    The returned builder reads a host component's latest value through the
    dialect-resolved StateService, then delivers it to a supplied callback.

    :param dialect: The host-dialect flag used for StateService resolution.
    :type dialect: str
    :param di_context: Optional resolver override for explicit composition.
    :type di_context: Any | None
    :return: A builder for state-backed host callbacks.
    :rtype: Callable[[str, Callable[[Any], Any]], Callable[[], Any]]
    '''

    # Resolve the configured state service for the requested host dialect.
    di_context = di_context if di_context is not None else create_di_context()
    state_service = di_context.get_dependency(STATE_SERVICE_ID, dialect)

    # Build the zero-argument callback Streamlit invokes after a value change.
    def build_handler(key: str, callback: Callable[[Any], Any]) -> Callable[[], Any]:
        '''
        Bind a component session-state key to a payload consumer.

        :param key: The Streamlit component's stable widget key.
        :type key: str
        :param callback: The consumer for the component's latest payload.
        :type callback: Callable[[Any], Any]
        :return: A zero-argument host callback.
        :rtype: Callable[[], Any]
        '''

        # Read the updated component payload only when the host invokes it.
        def handler() -> Any:
            '''Read the component payload and deliver it to the callback.'''

            # Retrieve the value through the dialect-resolved state service.
            payload = state_service.get(key)

            # Deliver the host report to the supplied agnostic consumer.
            return callback(payload)

        # Return the callback closure for host registration.
        return handler

    # Return the state-backed handler builder to the dialect-specific edge.
    return build_handler

# *** blueprints

# ** blueprint: build_frame
def build_frame(elements: list) -> Frame:
    '''
    Build one immutable Frame from recursive widget specifications.

    :param elements: The root widget specifications for the Frame.
    :type elements: list
    :return: The immutable Frame described by the specifications.
    :rtype: Frame
    '''

    # Delegate recursive Element and Frame construction to the domain event.
    return DomainEvent.handle(
        CreateFrame,
        elements=elements,
    )
