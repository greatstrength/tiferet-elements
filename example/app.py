"""Run with: streamlit run example/app.py."""

# *** imports

# ** infra
import streamlit as st

# ** app
from tiferet_elements.blueprints.core import build_frame
from tiferet_elements.blueprints.streamlit import build_streamlit_binding

# *** constants

# ** constant: gallery_widgets
GALLERY_WIDGETS = [
    (
        'button',
        {
            'widget_type': 'button',
            'props': {'children': 'BUTTON SAMPLE'},
        },
    ),
    (
        'text_field',
        {
            'widget_type': 'text_field',
            'props': {'label': 'TEXT FIELD SAMPLE'},
        },
    ),
    (
        'box',
        {
            'widget_type': 'box',
            'props': {'children': 'BOX SAMPLE'},
        },
    ),
    (
        'icon',
        {
            'widget_type': 'icon',
            'props': {'children': 'home'},
        },
    ),
    (
        'card',
        {
            'widget_type': 'card',
            'props': {'children': 'CARD SAMPLE'},
        },
    ),
    (
        'form_label',
        {
            'widget_type': 'form_label',
            'props': {'children': 'FORM LABEL SAMPLE'},
        },
    ),
    (
        'typography',
        {
            'widget_type': 'typography',
            'props': {'children': 'TYPOGRAPHY SAMPLE'},
        },
    ),
]

# *** functions

# ** function: render_gallery
def render_gallery() -> None:
    '''
    Render one catalogued instance of each Tiferet Elements widget type.

    :return: None
    :rtype: None
    '''

    # Configure the standalone gallery page before writing its content.
    st.set_page_config(
        page_title='Tiferet Elements Component Gallery',
        page_icon='🎨',
    )
    st.title('Tiferet Elements Component Gallery')

    # Build the single host-specific edge used to mount every composed Frame.
    binding = build_streamlit_binding()

    # Caption each catalog entry and mount it through the public blueprints.
    for widget_type, widget_spec in GALLERY_WIDGETS:
        st.caption(widget_type)
        binding(
            build_frame(elements=[widget_spec]),
            key=f'tiferet_elements_gallery_{widget_type}',
        )

# Render the standalone component gallery.
render_gallery()
