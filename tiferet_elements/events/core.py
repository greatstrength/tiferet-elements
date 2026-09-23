"""Tiferet Elements Callback Events."""

# *** imports

# ** app
from tiferet.events import DomainEvent
from .. import assets as a
from ..domain import Element
from ..mappers import ElementAggregate

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
