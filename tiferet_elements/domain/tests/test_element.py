# *** imports

# ** app
from tiferet_elements.domain import Element

# *** tests

# ** test: test_element_constructs_nested_children
def test_element_constructs_nested_children():
    '''
    Construct a nested Element tree from a child dict.
    '''

    # Construct a Box with a Button child supplied as a plain dict.
    element = Element(
        type='Box',
        props={'sx': {'padding': 2}},
        children=[{'type': 'Button', 'props': {'variant': 'contained'}}],
    )

    # Verify parent fields and recursive child construction.
    assert element.type == 'Box'
    assert element.props == {'sx': {'padding': 2}}
    assert isinstance(element.children[0], Element)
    assert element.children[0].type == 'Button'
