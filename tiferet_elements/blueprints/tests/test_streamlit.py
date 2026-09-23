"""Streamlit binding blueprint tests."""

# *** imports

# ** app
from tiferet_elements.blueprints.streamlit import build_streamlit_binding
from tiferet_elements.domain import Element, Frame

# *** tests

# ** test: binding_mounts_component_and_dispatches_host_report
def test_binding_mounts_component_and_dispatches_host_report(monkeypatch):
    '''Test that the binding mounts the component and dispatches its callback.'''

    # Record the declared component and its most recent mount arguments.
    declaration = {}
    component_call = {}

    def component(**kwargs):
        '''Record the component mount arguments.'''

        component_call.update(kwargs)
        return None

    def declare(name, path):
        '''Record the declared component identity and return its fake mount.'''

        declaration.update({'name': name, 'path': path})
        return component

    # Build a deterministic host callback around the binding's dispatch closure.
    def handler_builder(key, dispatch):
        '''Return a callback that reports one registered interaction.'''

        def on_change():
            '''Dispatch a serialized callback report from the fake host.'''

            return dispatch('{"callback_00": {}, "timestamp": 1788552865158}')

        return on_change

    # Replace only the Streamlit declaration boundary with the fake component.
    monkeypatch.setattr(
        'tiferet_elements.blueprints.streamlit.declare_component',
        declare,
    )
    handled = []
    frame = Frame(
        elements=[
            Element(
                type='Button',
                props={'onClick': lambda: handled.append('button clicked')},
            ),
        ],
    )

    # Build, mount, and invoke the host callback for the composed frame.
    binding = build_streamlit_binding(handler_builder=handler_builder)
    binding(frame, key='mui_demo')
    component_call['on_change']()

    # Verify component declaration, serialization, and callback dispatch.
    assert declaration['name'] == 'muiElements'
    assert declaration['path'].endswith('tiferet_elements/assets/streamlit')
    assert component_call['key'] == 'mui_demo'
    assert 'render("muiElements","Button"' in component_call['js']
    assert 'tiferet-material-icons' in component_call['js']
    assert './material-icons/material-icons.css' in component_call['js']
    assert handled == ['button clicked']

# ** test: binding_serializes_icon_ligature_name
def test_binding_serializes_icon_ligature_name(monkeypatch):
    '''Test that the binding preserves an Icon's Material Icons ligature name.'''

    # Record the fake component mount without requiring a Streamlit runtime.
    component_call = {}

    def component(**kwargs):
        '''Record the component mount arguments.'''

        component_call.update(kwargs)

    monkeypatch.setattr(
        'tiferet_elements.blueprints.streamlit.declare_component',
        lambda name, path: component,
    )
    frame = Frame(
        elements=[Element(type='Icon', props={'children': 'home'})],
    )

    # Mount the icon frame through a deterministic no-op host callback.
    binding = build_streamlit_binding(
        handler_builder=lambda key, dispatch: lambda: None,
    )
    binding(frame, key='mui_icon')

    # Verify icon rendering preserves the ligature name and stylesheet wrapper.
    assert 'render("muiElements","Icon"' in component_call['js']
    assert '"children":"home"' in component_call['js']
    assert 'tiferet-material-icons' in component_call['js']
