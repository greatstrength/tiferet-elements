"""Streamlit-specific Tiferet Elements utilities."""

# *** imports

# ** core
from pathlib import Path
from typing import Any

# ** infra
import streamlit as st

# ** app
from ..interfaces import StateService

# *** constants

# ** constant: material_icons_stylesheet_href
MATERIAL_ICONS_STYLESHEET_HREF = './material-icons/material-icons.css'

# *** functions

# ** function: get_streamlit_bundle_path
def get_streamlit_bundle_path() -> str:
    '''
    Return the absolute filesystem path of the vendored Streamlit bundle.

    Keeping the asset location beside this host-specific adapter lets the
    Streamlit blueprint declare the component without embedding a path.

    :return: The vendored component bundle path.
    :rtype: str
    '''

    # Resolve the package-relative frontend bundle for Streamlit's path API.
    return str(Path(__file__).parents[1] / 'assets' / 'streamlit')

# ** function: get_material_icons_font_path
def get_material_icons_font_path() -> str:
    '''
    Return the absolute filesystem path of the vendored Material Icons font.

    :return: The vendored Material Icons woff2 path.
    :rtype: str
    '''

    # Resolve the font beside the Streamlit component bundle.
    return str(
        Path(get_streamlit_bundle_path())
        / 'material-icons'
        / 'MaterialIcons-Regular.woff2'
    )

# ** function: wrap_js_with_material_icons_font
def wrap_js_with_material_icons_font(js: str) -> str:
    '''
    Wrap a render payload so the component iframe loads Material Icons.

    The vendored bundle evaluates the ``js`` argument as
    ``return (<js>);``. This wrapper stays a single expression that
    injects the local stylesheet once, then returns the original render
    array. Runtime injection is used instead of patching ``index.html``
    so regenerating the Next.js export does not drop the font.

    :param js: The serialized render-expression payload.
    :type js: str
    :return: The font-injecting JavaScript expression.
    :rtype: str
    '''

    # Inject the bundled stylesheet before returning the original renders.
    return (
        '(function(){'
        'if(!document.getElementById("tiferet-material-icons")){'
        'var link=document.createElement("link");'
        'link.id="tiferet-material-icons";'
        'link.rel="stylesheet";'
        f'link.href={MATERIAL_ICONS_STYLESHEET_HREF!r};'
        'document.head.appendChild(link);'
        '}'
        f'return {js};'
        '})()'
    )

# *** utils

# ** util: streamlit_state
class StreamlitState(StateService):
    '''
    Adapts Streamlit's rerun-persistent session state to the MUI state
    contract, keeping host state access behind the dialect-specific edge.
    '''

    # * method: get
    def get(self, key: str) -> Any:
        '''
        Retrieve a value from the active Streamlit session.

        :param key: The session-state key.
        :type key: str
        :return: The stored session-state value.
        :rtype: Any
        '''

        # Read the current value through Streamlit's session-state mapping.
        return st.session_state[key]

    # * method: set
    def set(self, key: str, value: Any) -> None:
        '''
        Store a value in the active Streamlit session.

        :param key: The session-state key.
        :type key: str
        :param value: The value to persist for the session.
        :type value: Any
        :return: None
        :rtype: None
        '''

        # Persist the value through Streamlit's session-state mapping.
        st.session_state[key] = value
