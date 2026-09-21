"""Tiferet Elements Element Domain Tests"""

# *** imports

# ** app
from tiferet_elements.domain import Element

# *** tests

# ** test: test_element_constructs_nested_children
def test_element_constructs_nested_children():
    '''
    Test Element recursively constructs child domain objects.
    '''

    # Construct a nested widget description from plain data.
    element = Element(
        type='Box',
        props={'sx': {'padding': 2}},
        children=[
            {
                'type': 'Button',
                'props': {'variant': 'contained'},
            },
        ],
    )

    # Verify recursive child validation preserves the described tree.
    assert element.type == 'Box'
    assert element.props == {'sx': {'padding': 2}}
    assert isinstance(element.children[0], Element)
    assert element.children[0].type == 'Button'
