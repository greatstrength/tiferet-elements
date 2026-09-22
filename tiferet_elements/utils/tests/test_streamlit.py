"""Streamlit utility tests."""

# *** imports

# ** core
from pathlib import Path

# ** infra
import streamlit as st

# ** app
from tiferet_elements.assets import ICON_ELEMENT_DEFAULTS
from tiferet_elements.interfaces import StateService
from tiferet_elements.utils.streamlit import (
    MATERIAL_ICONS_STYLESHEET_HREF,
    StreamlitState,
    get_material_icons_font_path,
    get_streamlit_bundle_path,
    wrap_js_with_material_icons_font,
)

# *** tests

# ** test: streamlit_state_proxies_session_state
def test_streamlit_state_proxies_session_state(monkeypatch):
    '''
    Test that StreamlitState proxies values through Streamlit session state.
    '''

    # Replace the Streamlit mapping with an isolated test session state.
    session_state = {}
    monkeypatch.setattr(st, 'session_state', session_state)

    # Store and retrieve a nested component callback state.
    state_service = StreamlitState()
    state_service.set('component', {'callback_00': {}})

    # Verify the service contract and direct backing-map proxy behavior.
    assert isinstance(state_service, StateService)
    assert state_service.get('component') == {'callback_00': {}}
    assert session_state['component'] == {'callback_00': {}}

# ** test: bundle_path_resolves_vendored_component
def test_bundle_path_resolves_vendored_component():
    '''
    Test that the vendored Streamlit component bundle resolves on disk.
    '''

    # Resolve the bundle path through the host-specific utility.
    bundle_path = get_streamlit_bundle_path()

    # Verify the expected package-relative location and entrypoint exist.
    assert bundle_path.endswith('tiferet_elements/assets/streamlit')
    assert (Path(bundle_path) / 'index.html').is_file()

# ** test: material_icons_font_is_vendored
def test_material_icons_font_is_vendored():
    '''
    Test that Material Icons font and stylesheet assets are vendored.
    '''

    # Resolve the font and stylesheet paths from the component bundle.
    font_path = Path(get_material_icons_font_path())
    stylesheet_path = (
        Path(get_streamlit_bundle_path())
        / 'material-icons'
        / 'material-icons.css'
    )

    # Verify the font, stylesheet, and Icon element defaults are available.
    assert font_path.is_file()
    assert font_path.read_bytes()[:4] == b'wOF2'
    assert stylesheet_path.is_file()
    assert "font-family: 'Material Icons'" in stylesheet_path.read_text()
    assert ICON_ELEMENT_DEFAULTS == {'type': 'Icon', 'props': {}}

# ** test: wrap_js_injects_material_icons_stylesheet
def test_wrap_js_injects_material_icons_stylesheet():
    '''
    Test that the JavaScript wrapper injects the Material Icons stylesheet.
    '''

    # Wrap an Icon render payload for component-iframe execution.
    wrapped_js = wrap_js_with_material_icons_font(
        '[render("muiElements","Icon")]',
    )

    # Verify the wrapper preserves the payload and injects the local font.
    assert wrapped_js.startswith('(function(){')
    assert wrapped_js.endswith('})()')
    assert 'tiferet-material-icons' in wrapped_js
    assert MATERIAL_ICONS_STYLESHEET_HREF in wrapped_js
    assert 'return [render("muiElements","Icon")];' in wrapped_js
