"""Tiferet Elements Element Domain Model"""

# *** imports

# ** core
from __future__ import annotations
from typing import Any, Dict, List

# ** infra
from pydantic import Field

# ** app
from tiferet.domain import DomainObject

# *** models

# ** model: element
class Element(DomainObject):
    '''
    Describes one host-agnostic widget node so callers can compose a UI tree
    without coupling its structure to a rendering runtime.
    '''

    # * attribute: type
    type: str = Field(..., description='The widget type rendered for this element.')

    # * attribute: props
    props: Dict[str, Any] = Field(
        default_factory=dict,
        description='The JSON-compatible properties supplied to the widget.',
    )

    # * attribute: children
    children: List[Element] = Field(
        default_factory=list,
        description='The child elements nested beneath this element.',
    )
