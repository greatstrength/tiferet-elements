"""Host-agnostic binding composition for Tiferet Elements."""
from __future__ import annotations

# *** imports

# ** core

from typing import TYPE_CHECKING, Any, Callable

# ** app
from tiferet.events import DomainEvent
from ..assets import STATE_SERVICE_ID
from ..di import create_elements_service_resolver
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
    Compose host callbacks that retrieve their latest state on invocation.

    :param dialect: The host dialect used to resolve the state service.
    :type dialect: str
    :param di_context: An optional dependency resolver override.
    :type di_context: Any
    :return: A function that builds state-aware host callback handlers.
    :rtype: Callable[[str, Callable[[Any], Any]], Callable[[], Any]]
    '''

    # Resolve the supplied dependency resolver or compose the default resolver.
    di_context = (
        di_context
        if di_context is not None
        else create_elements_service_resolver()
    )

    # Resolve the dialect-specific state service once for all built handlers.
    state_service = di_context.get_dependency(STATE_SERVICE_ID, dialect)

    # Build a host handler for one component key and domain callback.
    def build_handler(
            key: str,
            callback: Callable[[Any], Any],
        ) -> Callable[[], Any]:
        '''
        Build a zero-argument handler that forwards current component state.

        :param key: The component key whose reported state to retrieve.
        :type key: str
        :param callback: The domain callback that receives the reported state.
        :type callback: Callable[[Any], Any]
        :return: A zero-argument host callback handler.
        :rtype: Callable[[], Any]
        '''

        # Read the latest reported payload before dispatching it to the callback.
        def handler() -> Any:
            '''Forward the latest state payload to the configured callback.'''

            return callback(state_service.get(key))

        # Return the composed zero-argument host callback.
        return handler

    # Return the handler builder bound to the resolved state service.
    return build_handler

# *** blueprints

# ** blueprint: build_frame
def build_frame(elements: list) -> Frame:
    '''
    Materialize a host-agnostic Frame from plain widget specifications.

    :param elements: The root widget specifications composing the frame.
    :type elements: list
    :return: The immutable Frame materialized from the specifications.
    :rtype: Frame
    '''

    # Delegate frame materialization to the domain event composition surface.
    return DomainEvent.handle(CreateFrame, elements=elements)
