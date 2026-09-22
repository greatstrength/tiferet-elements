"""Tiferet Elements Mapper Test Configuration"""

# *** imports

# ** app
from tiferet.testing import register_mapper_hooks

# *** functions

# ** function: pytest_generate_tests
def pytest_generate_tests(metafunc):
    register_mapper_hooks(metafunc)

# ** function: element_tree
def element_tree(element):
    '''
    Normalize a nested Element or element dictionary into a comparable tree.

    :param element: The Element model or equivalent dictionary.
    :type element: Element | dict
    :return: The comparable recursive element tuple.
    :rtype: tuple
    '''

    # Read the element values from either its model or serialized dictionary.
    if isinstance(element, dict):
        element_type = element['type']
        props = element.get('props', {})
        children = element.get('children', [])
    else:
        element_type = element.type
        props = element.props
        children = element.children

    # Normalize each child into the same recursive shape.
    return element_type, props, tuple(element_tree(child) for child in children)

# ** function: primary_handler
def primary_handler(**kwargs):
    '''
    Return primary callback parameters unchanged.

    :param kwargs: Callback parameters.
    :type kwargs: dict
    :return: The unchanged callback parameters.
    :rtype: dict
    '''

    # Return the callback parameters unchanged.
    return kwargs

# ** function: secondary_handler
def secondary_handler(**kwargs):
    '''
    Return secondary callback parameters unchanged.

    :param kwargs: Callback parameters.
    :type kwargs: dict
    :return: The unchanged callback parameters.
    :rtype: dict
    '''

    # Return the callback parameters unchanged.
    return kwargs
