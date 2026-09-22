"""Tiferet Elements Frame Domain Model"""

# *** imports

# ** core
from typing import List

# ** infra
from pydantic import Field

# ** app
from tiferet.domain import DomainObject
from .element import Element

# *** models

# ** model: frame
class Frame(DomainObject):
    '''
    Captures the freshly composed element tree for one render pass, keeping
    rendered structure and registered interactions aligned.
    '''

    # * attribute: elements
    elements: List[Element] = Field(
        default_factory=list,
        description='The root elements composing this render pass.',
    )
