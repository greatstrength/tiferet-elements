"""Tiferet Elements Callback Table Domain Model"""

# *** imports

# ** core
from typing import Any, Callable, Dict

# ** infra
from pydantic import Field

# ** app
from tiferet.domain import DomainObject

# *** models

# ** model: callback_table
class CallbackTable(DomainObject):
    '''
    Preserves the handler snapshot for one frame so a reported callback ID can
    be resolved without host-specific callback wiring.
    '''

    # * attribute: handlers
    handlers: Dict[str, Callable[..., Any]] = Field(
        default_factory=dict,
        description='The callback-ID-to-handler mapping for the render pass.',
    )
