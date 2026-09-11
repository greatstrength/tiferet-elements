# tiferet-elements

Tiferet Elements lets a Streamlit application describe and render Material UI, Nivo, and Monaco widgets through Streamlit's supported public component API. It keeps widget trees and callback routing host-agnostic, while the optional Streamlit binding handles mounting and interaction delivery.

## Install

Install the core package when you only need its domain models, widget defaults, and domain events:

```bash
pip install tiferet-elements
```

Install the Streamlit extra to render a `Frame` in a Streamlit application:

```bash
pip install "tiferet-elements[streamlit]"
```

## Minimal usage

Build a nested Frame from widget specifications, then mount it with the Streamlit binding:

```python
from tiferet_elements.blueprints.core import build_frame
from tiferet_elements.blueprints.streamlit import build_streamlit_binding


def save() -> None:
    print('Saved.')


frame = build_frame(
    elements=[
        {
            'widget_type': 'box',
            'props': {'sx': {'display': 'grid', 'gap': 2}},
            'children': [
                {
                    'widget_type': 'text_field',
                    'props': {'label': 'Name', 'fullWidth': True},
                },
                {
                    'widget_type': 'button',
                    'props': {'children': 'Save', 'onClick': save},
                },
            ],
        },
    ],
)

build_streamlit_binding()(frame, key='profile_form')
```

Run the included interactive example with:

```bash
streamlit run examples/streamlit_binding_demo.py
```
