"""Streamlit utility tests."""

# *** imports

# ** core
from pathlib import Path

# ** infra
import streamlit as st

# ** app
from tiferet_mui.assets import ICON_ELEMENT_DEFAULTS
from tiferet_mui.interfaces import StateService
from tiferet_mui.utils.streamlit import (
    MATERIAL_ICONS_STYLESHEET_HREF,
    StreamlitState,
    get_material_icons_font_path,
    get_streamlit_bundle_path,
    wrap_js_with_material_icons_font,
)

# *** tests

# ** test: test_streamlit_state_proxies_session_state
def test_streamlit_state_proxies_session_state(monkeypatch):
    '''Test StreamlitState reads and writes the current Streamlit state mapping.'''

    # Replace Streamlit's runtime state proxy with a deterministic mapping.
    session_state = {}
    monkeypatch.setattr(st, 'session_state', session_state)
    state_service = StreamlitState()

    # Store and retrieve a value through the StateService contract.
    state_service.set('component', {'callback_00': {}})

    # Verify the adapter remains a StateService and proxies its backing mapping.
    assert isinstance(state_service, StateService)
    assert state_service.get('component') == {'callback_00': {}}
    assert session_state['component'] == {'callback_00': {}}

# ** test: test_bundle_path_resolves_vendored_component
def test_bundle_path_resolves_vendored_component():
    '''Test the component path resolves to the packaged frontend entrypoint.'''

    # Resolve the filesystem path supplied to declare_component.
    bundle_path = get_streamlit_bundle_path()

    # Verify the vendored frontend entrypoint exists at that path.
    assert bundle_path.endswith('tiferet_mui/assets/streamlit')
    assert (Path(bundle_path) / 'index.html').is_file()

# ** test: test_material_icons_font_is_vendored
def test_material_icons_font_is_vendored():
    '''Test the Material Icons font and stylesheet ship with the component.'''

    # Resolve the vendored font next to the Streamlit bundle.
    font_path = Path(get_material_icons_font_path())
    stylesheet_path = (
        Path(get_streamlit_bundle_path()) / 'material-icons' / 'material-icons.css'
    )

    # Verify the woff2, stylesheet, and unchanged Icon catalog shape.
    assert font_path.is_file()
    assert font_path.read_bytes()[:4] == b'wOF2'
    assert stylesheet_path.is_file()
    assert "font-family: 'Material Icons'" in stylesheet_path.read_text()
    assert ICON_ELEMENT_DEFAULTS == {
        'type': 'Icon',
        'props': {},
    }

# ** test: test_wrap_js_injects_material_icons_stylesheet
def test_wrap_js_injects_material_icons_stylesheet():
    '''Test the js wrapper injects the local stylesheet around render expressions.'''

    # Wrap a representative render payload the bundle will evaluate.
    wrapped = wrap_js_with_material_icons_font('[render("muiElements","Icon")]')

    # Verify the original payload is returned after a one-time stylesheet inject.
    assert wrapped.startswith('(function(){')
    assert wrapped.endswith('})()')
    assert 'tiferet-material-icons' in wrapped
    assert MATERIAL_ICONS_STYLESHEET_HREF in wrapped
    assert 'return [render("muiElements","Icon")];' in wrapped
