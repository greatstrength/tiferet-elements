"""Tiferet Elements Element Mappers."""

# *** imports

# ** core
from typing import Any, Dict, List

# ** app
from tiferet.mappers import Aggregate

from ..domain import Element

# *** mappers

# ** mapper: element_aggregate
class ElementAggregate(Element, Aggregate):
    '''
    Provides a validated mutation surface while an Element is composed before
    callers receive its immutable domain snapshot.
    '''

    # * method: set_type
    def set_type(self, type: str) -> None:
        '''
        Set the Material UI widget type.

        :param type: The Material UI widget type.
        :type type: str
        :return: None
        :rtype: None
        '''

        # Apply the validated widget-type mutation.
        self.set_attribute('type', type)

    # * method: set_props
    def set_props(self, props: Dict[str, Any]) -> None:
        '''
        Set the Material UI widget properties.

        :param props: The JSON-compatible properties for the widget.
        :type props: Dict[str, Any]
        :return: None
        :rtype: None
        '''

        # Apply the validated properties mutation.
        self.set_attribute('props', props)

    # * method: set_children
    def set_children(self, children: List[Element]) -> None:
        '''
        Set the nested Elements below this widget.

        :param children: The nested Element descriptions.
        :type children: List[Element]
        :return: None
        :rtype: None
        '''

        # Apply the validated child-elements mutation.
        self.set_attribute('children', children)

    # * method: freeze
    def freeze(self) -> Element:
        '''
        Freeze the working Element into an independent domain snapshot.

        :return: The immutable Element domain object.
        :rtype: Element
        '''

        # Copy mutable values so later aggregate changes cannot affect the snapshot.
        return Element(
            type=self.type,
            props=dict(self.props),
            children=list(self.children),
        )
