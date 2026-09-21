# Tiferet Elements Component Gallery

A runnable Streamlit gallery that renders every widget currently available in
the Tiferet Elements catalog.

## Prerequisites

- Python 3.10+
- `tiferet-elements` installed with its Streamlit extra

## Setup

From the repository root, install the package and its optional Streamlit
dependency:

```bash
pip install -e '.[streamlit]'
```

## Running

From the repository root:

```bash
streamlit run example/app.py
```

## What to Expect

The page captions and renders one instance of each widget type:

- `button` — Material UI `Button`
- `text_field` — Material UI `TextField`
- `box` — Material UI `Box`
- `icon` — Material UI `Icon`, rendered from the vendored Material Icons font
- `card` — Material UI `Card`
- `form_label` — Material UI `FormLabel`, the catalog's real MUI
  label-equivalent
- `typography` — Material UI `Typography`

## Architecture

- `app.py` builds each widget specification through `build_frame` and mounts it
  through `build_streamlit_binding`.
- `../tiferet_elements/assets/core.py` contains the host-agnostic default data for
  every catalogued widget type.
- `../tiferet_elements/events/core.py` materializes the specifications into
  immutable Elements and Frames.
- `../tiferet_elements/blueprints/streamlit.py` adapts a Frame to the vendored
  Streamlit component.
