"""Tiferet Elements Frame Domain Tests"""

# *** imports

# ** app
from tiferet_elements.domain import Element, Frame

# *** tests

# ** test: test_frame_constructs_render_pass
def test_frame_constructs_render_pass():
    '''
    Test Frame stores the root elements for one render pass.
    '''

    # Construct a frame from a caller-authored root element.
    frame = Frame(
        elements=[
            Element(
                type='Stack',
                children=[
                    Element(type='TextField'),
                ],
            ),
        ],
    )

    # Verify the composed tree remains available on the frame.
    assert len(frame.elements) == 1
    assert frame.elements[0].type == 'Stack'
    assert frame.elements[0].children[0].type == 'TextField'
