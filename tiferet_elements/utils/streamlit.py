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

    :return: The absolute vendored Streamlit bundle path.
    :rtype: str
    '''

    # Resolve the vendored frontend bundle beside the package assets.
    return str(Path(__file__).parents[1] / 'assets' / 'streamlit')


# ** function: get_material_icons_font_path
def get_material_icons_font_path() -> str:
    '''
    Return the absolute filesystem path of the vendored Material Icons font.

    :return: The absolute vendored Material Icons font path.
    :rtype: str
    '''

    # Resolve the font relative to the vendored component bundle.
    return str(
        Path(get_streamlit_bundle_path())
        / 'material-icons'
        / 'MaterialIcons-Regular.woff2'
    )


# ** function: wrap_js_with_material_icons_font
def wrap_js_with_material_icons_font(js: str) -> str:
    '''
    Wrap a render payload so the component iframe loads Material Icons.

    The vendored bundle evaluates ``js`` as ``return (<js>);``. This wrapper
    remains a single expression that injects the local stylesheet once, then
    returns the original render array. Runtime injection preserves the font
    when the Next.js export is regenerated.

    :param js: The JavaScript expression that produces the render array.
    :type js: str
    :return: The wrapped JavaScript expression.
    :rtype: str
    '''

    # Inject the local Material Icons stylesheet before returning the payload.
    return (
        f'(function(){{if(!document.getElementById("tiferet-material-icons"))'
        f'{{var link=document.createElement("link");'
        f'link.id="tiferet-material-icons";link.rel="stylesheet";'
        f'link.href={MATERIAL_ICONS_STYLESHEET_HREF!r};'
        f'document.head.appendChild(link);}}return {js};}})()'
    )


# *** utils

# ** util: streamlit_state
class StreamlitState(StateService):
    '''
    Adapt Streamlit's rerun-persistent session state to the MUI state contract.

    This keeps host state access behind the dialect-specific edge.
    '''

    # * method: get
    def get(self, key: str) -> Any:
        '''
        Retrieve a Streamlit session-state value by key.

        :param key: The session-state key.
        :type key: str
        :return: The stored value.
        :rtype: Any
        '''

        # Retrieve the value from Streamlit's persistent session state.
        return st.session_state[key]

    # * method: set
    def set(self, key: str, value: Any) -> None:
        '''
        Store a Streamlit session-state value by key.

        :param key: The session-state key.
        :type key: str
        :param value: The value to store.
        :type value: Any
        :return: None
        :rtype: None
        '''

        # Store the value in Streamlit's persistent session state.
        st.session_state[key] = value
