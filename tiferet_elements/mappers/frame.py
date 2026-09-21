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
        Add one root Element to the composed Frame.

        :param element: The Element to add to the Frame.
        :type element: Element
        :return: None
        :rtype: None
        '''

        # Copy the current tree before adding the next root Element.
        elements = list(self.elements)
        elements.append(element)

        # Apply the validated root-elements mutation.
        self.set_attribute('elements', elements)

    # * method: freeze
    def freeze(self) -> Frame:
        '''
        Freeze the working Frame into an independent domain snapshot.

        :return: The immutable Frame domain object.
        :rtype: Frame
        '''

        # Copy root Elements so later aggregate additions do not affect the snapshot.
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
        'to_data': {
            'mode': 'json',
        },
    }

    # * method: map
    def map(self, **overrides) -> Frame:
        '''
        Map the serialized frame data to its domain representation.

        :param overrides: Additional field values that override serialized data.
        :type overrides: dict
        :return: The mapped frame domain object.
        :rtype: Frame
        '''

        # Construct the domain frame through the shared transfer-object path.
        return super().map(Frame, **overrides)

    # * method: from_model
    @classmethod
    def from_model(cls, frame: Frame, **overrides) -> 'FrameTransferObject':
        '''
        Create a transfer object from a composed frame.

        :param frame: The composed frame domain object.
        :type frame: Frame
        :param overrides: Additional field values that override model data.
        :type overrides: dict
        :return: The frame transfer object.
        :rtype: FrameTransferObject
        '''

        # Convert the domain frame through the shared transfer-object path.
        return super().from_model(frame, **overrides)
