"""Tiferet Elements Callback Events."""

# *** imports

# ** core
from typing import Any, Callable, Iterator, Tuple

# ** app
from tiferet.events import DomainEvent
from .. import assets as a
from ..domain import CallbackTable, Element, Frame
from ..mappers import CallbackTableAggregate, ElementAggregate, FrameAggregate

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
        Create an Element by merging a widget's defaults with caller overrides.

        :param widget_type: The catalog identifier of the widget to create.
        :type widget_type: str
        :param props: Caller-supplied properties that override widget defaults.
        :type props: dict
        :param children: Nested child elements for the resulting Element.
        :type children: list
        :param kwargs: Additional event arguments.
        :type kwargs: dict
        :return: The immutable Element composed from the widget defaults.
        :rtype: Element
        '''

        # Look up the configured defaults for the requested widget type.
        defaults = a.WIDGET_ELEMENT_DEFAULTS.get(widget_type)

        # Report the requested widget type when no defaults are registered.
        if defaults is None:
            self.raise_error(
                a.WIDGET_TYPE_NOT_FOUND_ID,
                widget_type=widget_type,
            )

        # Overlay caller properties onto the widget's default properties.
        element_props = {**defaults['props'], **(props or {})}

        # Preserve supplied children while defaulting omitted children to empty.
        element_children = children if children is not None else []

        # Compose the mutable element through its validated aggregate surface.
        element = ElementAggregate(type='')
        element.set_type(defaults['type'])
        element.set_props(element_props)
        element.set_children(element_children)

        # Return the immutable Element snapshot to the caller.
        return element.freeze()


# ** event: create_frame
class CreateFrame(DomainEvent):
    '''Materialize a nested Frame from recursive widget specification data.'''

    # * method: execute
    @DomainEvent.parameters_required(['elements'])
    def execute(self, elements: list, **kwargs) -> Frame:
        '''
        Create a Frame from recursive widget specifications.

        :param elements: The root widget specifications to materialize.
        :type elements: list
        :param kwargs: Additional event arguments.
        :type kwargs: dict
        :return: The immutable Frame composed from the widget specifications.
        :rtype: Frame
        '''

        # Create the mutable frame composition surface.
        frame = FrameAggregate()

        # Materialize and append every root element specification.
        for element_spec in elements:
            frame.add_element(self._create_element(element_spec))

        # Return the immutable frame snapshot to the caller.
        return frame.freeze()

    # * method: _create_element (static)
    @staticmethod
    def _create_element(element_spec: dict) -> Element:
        '''
        Recursively materialize an Element from one widget specification.

        :param element_spec: The widget specification to materialize.
        :type element_spec: dict
        :return: The immutable Element represented by the specification.
        :rtype: Element
        '''

        # Materialize nested child specifications before their parent node.
        children = [
            CreateFrame._create_element(child)
            for child in element_spec.get('children', [])
        ]

        # Delegate widget defaults and error handling to CreateElement.
        return DomainEvent.handle(
            CreateElement,
            widget_type=element_spec['widget_type'],
            props=element_spec.get('props'),
            children=children,
        )


# ** event: build_callback_table
class BuildCallbackTable(DomainEvent):
    '''Turns the callable-bearing elements of one frame into a stable, frozen
    callback registry that the host can safely render and later dispatch.'''

    # * method: execute
    @DomainEvent.parameters_required(['frame'])
    def execute(self, frame: Frame, **kwargs) -> CallbackTable:
        '''
        Build a frozen callback registry for every callable in a Frame.

        :param frame: The composed frame whose callback handlers to register.
        :type frame: Frame
        :param kwargs: Additional event arguments.
        :type kwargs: dict
        :return: The immutable callback registry for the rendered frame.
        :rtype: CallbackTable
        '''

        # Verify the callback registry is built from a composed frame.
        self.verify(
            expression=isinstance(frame, Frame),
            error_code=a.CALLBACK_NOT_FOUND_ID,
            message='A callback table can only be built from a Frame.',
        )

        # Create the mutable callback registration surface and first index.
        callback_table = CallbackTableAggregate()
        callback_index = 0

        # Register each callable in depth-first element-tree order.
        for element in self._walk(frame.elements):
            handler_prop, handler = self._get_handler(element)
            if handler is None:
                continue

            callback_id = f'callback_{callback_index:02d}'
            callback_table.register(callback_id, handler)
            element.props[handler_prop] = callback_id
            element.props['callback_id'] = callback_id
            callback_index += 1

        # Return the immutable callback registry for later dispatch.
        return callback_table.freeze()

    # * method: _walk (static)
    @staticmethod
    def _walk(elements: list[Element]) -> Iterator[Element]:
        '''
        Yield every Element in depth-first, pre-order tree traversal.

        :param elements: The sibling elements at the current tree level.
        :type elements: list[Element]
        :return: An iterator yielding each Element before its descendants.
        :rtype: Iterator[Element]
        '''

        # Yield each element before recursively yielding its descendants.
        for element in elements:
            yield element
            yield from BuildCallbackTable._walk(element.children)

    # * method: _get_handler (static)
    @staticmethod
    def _get_handler(element: Element) -> Tuple[str | None, Callable[..., Any] | None]:
        '''
        Find the first callable property belonging to an Element.

        :param element: The element whose properties are inspected.
        :type element: Element
        :return: The callable property name and handler, or empty values.
        :rtype: Tuple[str | None, Callable[..., Any] | None]
        '''

        # Return the first callable property available on the element.
        for prop_name, value in element.props.items():
            if callable(value):
                return prop_name, value

        # Report that the element has no callback handler.
        return None, None
