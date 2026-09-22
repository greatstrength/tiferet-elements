# *** imports

# ** app
from tiferet_elements.domain import Element, Frame

# *** tests

# ** test: test_frame_constructs_render_pass
def test_frame_constructs_render_pass():
    '''
    Construct a Frame for one render pass of nested elements.
    '''

    # Construct a Frame whose root is a Stack wrapping a TextField.
    frame = Frame(
        elements=[Element(type='Stack', children=[Element(type='TextField')])],
    )

    # Verify the root element list and nested child type.
    assert len(frame.elements) == 1
    assert frame.elements[0].type == 'Stack'
    assert frame.elements[0].children[0].type == 'TextField'
