"""Tiferet Elements Callback Events."""

# *** imports

# ** core
from typing import Any, Callable, Dict, Iterator, Tuple

# ** app
from tiferet.events import DomainEvent

from .. import assets as a
from ..domain import CallbackTable, Element, Frame
from ..mappers import (
    CallbackTableAggregate,
    ElementAggregate,
    FrameAggregate,
)

# *** events

# ** event: create_element
class CreateElement(DomainEvent):
    '''Materialize a host-agnostic Element from a catalogued widget default.'''

    # * method: execute
    @DomainEvent.parameters_required(['widget_type'])
    def execute(
            self,
            widget_type: str,
            props: dict = None,
            children: list = None,
            **kwargs,
        ) -> Element:
        '''
        Create an Element using one widget type's default data.

        The ``children`` parameter describes nested Element nodes. A
        ``children`` key inside ``props`` remains an ordinary Material UI prop,
        such as a Button label.

        :param widget_type: The catalog key for the Element default data.
        :type widget_type: str
        :param props: Properties that override the widget type's defaults.
        :type props: dict | None
        :param children: Elements nested beneath the created Element.
        :type children: list | None
        :param kwargs: Additional event parameters.
        :type kwargs: dict
        :return: The Element materialized from defaults and overrides.
        :rtype: Element
        '''

        # Resolve the default Element data assigned to the requested widget type.
        defaults = a.WIDGET_ELEMENT_DEFAULTS.get(widget_type)

        # Report unknown widget types instead of silently creating invalid data.
        if defaults is None:
            self.raise_error(
                a.WIDGET_TYPE_NOT_FOUND_ID,
                widget_type=widget_type,
            )

        # Merge default and caller properties without conflating Element children.
        element_props = {
            **defaults['props'],
            **(props or {}),
        }
        element_children = children if children is not None else []

        # Compose the Element through its validated aggregate mutation surface.
        element = ElementAggregate(type='')
        element.set_type(defaults['type'])
        element.set_props(element_props)
        element.set_children(element_children)

        # Return the aggregate's immutable Element snapshot.
        return element.freeze()

# ** event: create_frame
class CreateFrame(DomainEvent):
    '''Materialize a nested Frame from recursive widget specification data.'''

    # * method: execute
    @DomainEvent.parameters_required(['elements'])
    def execute(self, elements: list, **kwargs) -> Frame:
        '''
        Create a Frame from recursive widget specifications.

        :param elements: The root widget specifications for the Frame.
        :type elements: list
        :param kwargs: Additional event parameters.
        :type kwargs: dict
        :return: The immutable Frame described by the specifications.
        :rtype: Frame
        '''

        # Build each root Element before adding it to the mutable Frame aggregate.
        frame = FrameAggregate()
        for element_spec in elements:
            frame.add_element(self._create_element(element_spec))

        # Return the aggregate's immutable Frame snapshot.
        return frame.freeze()

    # * method: _create_element (static)
    @staticmethod
    def _create_element(element_spec: dict) -> Element:
        '''
        Materialize one recursive widget specification.

        :param element_spec: One widget specification and its nested children.
        :type element_spec: dict
        :return: The materialized Element.
        :rtype: Element
        '''

        # Materialize nested specifications before constructing this Element.
        children = [
            CreateFrame._create_element(child)
            for child in element_spec.get('children', [])
        ]

        # Reuse CreateElement so defaults and unknown-widget errors stay central.
        return DomainEvent.handle(
            CreateElement,
            widget_type=element_spec['widget_type'],
            props=element_spec.get('props'),
            children=children,
        )

# ** event: build_callback_table
class BuildCallbackTable(DomainEvent):
    '''
    Turns the callable-bearing elements of one frame into a stable, frozen
    callback registry that the host can safely render and later dispatch.
    '''

    # * method: execute
    @DomainEvent.parameters_required(['frame'])
    def execute(self, frame: Frame, **kwargs) -> CallbackTable:
        '''
        Build a callback table from the frame's interactive element tree.

        Each callable element prop marks an interactive element. The callable
        is registered under a generated identifier and replaced in the prop
        mapping with that identifier, preserving a JSON-safe render payload.

        :param frame: The composed frame whose element tree is registered.
        :type frame: Frame
        :param kwargs: Additional event parameters.
        :type kwargs: dict
        :return: The frozen callback table for the frame.
        :rtype: CallbackTable
        '''

        # Verify the required value is a composed frame before walking it.
        self.verify(
            expression=isinstance(frame, Frame),
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback table can only be built from a Frame.',
        )

        # Build registrations while assigning identifiers in tree-walk order.
        callback_table = CallbackTableAggregate()
        callback_index = 0
        for element in self._walk(frame.elements):
            handler_prop, handler = self._get_handler(element)
            if handler is None:
                continue

            callback_id = f'callback_{callback_index:02d}'
            callback_table.register(callback_id, handler)
            element.props[handler_prop] = callback_id
            element.props['callback_id'] = callback_id
            callback_index += 1

        # Return the aggregate's immutable domain snapshot.
        return callback_table.freeze()

    # * method: _walk (static)
    @staticmethod
    def _walk(elements: list[Element]) -> Iterator[Element]:
        '''
        Yield every element in depth-first tree-walk order.

        :param elements: The elements at the current tree depth.
        :type elements: list[Element]
        :return: An iterator over each element in the tree.
        :rtype: Iterator[Element]
        '''

        # Yield the current element before recursively yielding its descendants.
        for element in elements:
            yield element
            yield from BuildCallbackTable._walk(element.children)

    # * method: _get_handler (static)
    @staticmethod
    def _get_handler(element: Element) -> Tuple[str | None, Callable[..., Any] | None]:
        '''
        Find the first callable prop that makes an element interactive.

        :param element: The element whose props are inspected.
        :type element: Element
        :return: The handler-prop name and callable, when present.
        :rtype: Tuple[str | None, Callable[..., Any] | None]
        '''

        # Return the first callable property without branching by widget type.
        for prop_name, value in element.props.items():
            if callable(value):
                return prop_name, value

        # Report that the element has no registered interaction.
        return None, None

# ** event: dispatch_callback
class DispatchCallback(DomainEvent):
    '''
    Delivers one reported interaction to the handler registered for its
    callback identifier, making unclaimed interactions explicit domain errors.
    '''

    # * method: execute
    @DomainEvent.parameters_required(['callback_table', 'payload'])
    def execute(
            self,
            callback_table: CallbackTable,
            payload: Dict[str, Any],
            **kwargs,
        ) -> Any:
        '''
        Resolve and invoke the handler for one composite interaction payload.

        :param callback_table: The callback snapshot for the current frame.
        :type callback_table: CallbackTable
        :param payload: The payload containing one callback ID and a timestamp.
        :type payload: Dict[str, Any]
        :param kwargs: Additional event parameters.
        :type kwargs: dict
        :return: The value returned by the registered handler.
        :rtype: Any
        '''

        # Verify the payload uses the confirmed composite mapping shape.
        self.verify(
            expression=isinstance(payload, dict),
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback payload must be a mapping.',
        )
        self.verify(
            expression='timestamp' in payload,
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback payload must include a timestamp.',
        )

        # Resolve the single callback entry defined by the confirmed payload shape.
        callback_entries = [
            (callback_id, parameters)
            for callback_id, parameters in payload.items()
            if callback_id != 'timestamp'
        ]
        self.verify(
            expression=len(callback_entries) == 1,
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback payload must contain exactly one callback_id.',
        )
        callback_id, parameters = callback_entries[0]

        # Resolve the registered handler or report the unclaimed interaction.
        handler = callback_table.handlers.get(callback_id)
        if handler is None:
            self.raise_error(
                a.CALLBACK_NOT_FOUND_ID,
                callback_id=callback_id,
            )

        # Invoke the resolved handler with the callback-defined parameters.
        return handler(**parameters)
