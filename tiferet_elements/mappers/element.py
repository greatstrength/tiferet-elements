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
        Set the element type.

        :param type: The widget type rendered for this element.
        :type type: str
        :return: None
        :rtype: None
        '''

        # Validate and set the element type.
        self.set_attribute('type', type)

    # * method: set_props
    def set_props(self, props: Dict[str, Any]) -> None:
        '''
        Set the element properties.

        :param props: The JSON-compatible properties supplied to the widget.
        :type props: Dict[str, Any]
        :return: None
        :rtype: None
        '''

        # Validate and set the element properties.
        self.set_attribute('props', props)

    # * method: set_children
    def set_children(self, children: List[Element]) -> None:
        '''
        Set the nested child elements.

        :param children: The child elements nested beneath this element.
        :type children: List[Element]
        :return: None
        :rtype: None
        '''

        # Validate and set the nested child elements.
        self.set_attribute('children', children)

    # * method: freeze
    def freeze(self) -> Element:
        '''
        Freeze the current element composition into an immutable domain snapshot.

        :return: The immutable Element snapshot.
        :rtype: Element
        '''

        # Copy mutable containers into the immutable domain snapshot.
        return Element(
            type=self.type,
            props=dict(self.props),
            children=list(self.children),
        )
