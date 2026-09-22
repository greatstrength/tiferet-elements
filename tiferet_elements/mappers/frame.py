"""Tiferet Elements Frame Mappers"""

# *** imports

# ** core
from typing import Any, ClassVar, Dict

# ** app
from tiferet.mappers import Aggregate, TransferObject
from ..domain import Element, Frame

# *** mappers

# ** mapper: frame_aggregate
class FrameAggregate(Frame, Aggregate):
    '''
    Provides a validated mutation surface while a Frame is composed one Element
    at a time before callers receive its immutable domain snapshot.
    '''

    # * method: add_element
    def add_element(self, element: Element) -> None:
        '''
        Add an element to the frame.

        :param element: The root element to add to this frame.
        :type element: Element
        :return: None
        :rtype: None
        '''

        # Copy the current root elements before extending the composition.
        elements = list(self.elements)
        elements.append(element)

        # Validate and store the extended root element list.
        self.set_attribute('elements', elements)

    # * method: freeze
    def freeze(self) -> Frame:
        '''
        Freeze the current frame composition into an immutable domain snapshot.

        :return: The immutable Frame snapshot.
        :rtype: Frame
        '''

        # Copy the root elements into the immutable domain snapshot.
        return Frame(elements=list(self.elements))


# ** mapper: frame_transfer_object
class FrameTransferObject(Frame, TransferObject):
    '''
    Converts a frame into the JSON-safe recursive props tree the binding passes
    to the frontend, while retaining a direct path back to the domain shape.
    '''

    # * attribute: _ROLES
    _ROLES: ClassVar[Dict[str, Dict[str, Any]]] = {
        'to_model': {},
        'to_data': {'mode': 'json'},
    }

    # * method: map
    def map(self, **overrides) -> Frame:
        '''
        Map frame transfer data to its domain representation.

        :param overrides: Additional field overrides.
        :type overrides: dict
        :return: The mapped Frame.
        :rtype: Frame
        '''

        # Map the complete transfer-object shape to its domain type.
        return super().map(Frame, **overrides)

    # * method: from_model
    @classmethod
    def from_model(cls, frame: Frame, **overrides) -> 'FrameTransferObject':
        '''
        Create frame transfer data from a Frame domain model.

        :param frame: The source Frame domain model.
        :type frame: Frame
        :param overrides: Additional field overrides.
        :type overrides: dict
        :return: The constructed FrameTransferObject.
        :rtype: FrameTransferObject
        '''

        # Delegate model conversion to the generic transfer-object factory.
        return super().from_model(frame, **overrides)
