"""Streamlit binding blueprint for Tiferet Elements frames."""

# *** imports

# ** core
import json
from typing import Any, Callable

# ** infra
from streamlit.components.v1 import declare_component

# ** app
from ..events import BuildCallbackTable, DispatchCallback
from ..utils.streamlit import (
    get_streamlit_bundle_path,
    wrap_js_with_material_icons_font,
)
from .core import build_handler_builder

# *** functions

# ** function: _serialize_element
def _serialize_element(element: Any) -> str:
    '''Serialize one element tree to the vendored component render expression.'''

    # Serialize descendants before embedding them in the parent render call.
    children = ','.join(
        _serialize_element(child)
        for child in element.children
    )

    # Serialize element properties, including registered callback expressions.
    props = _serialize_props(element.props)

    # Return the Material UI renderer expression for this element.
    return (
        f'render("muiElements",{json.dumps(element.type)},{props},'
        f'[{children}])'
    )

# ** function: _serialize_props
def _serialize_props(props: dict[str, Any]) -> str:
    '''Serialize element properties, replacing registered handlers with senders.'''

    # Resolve the callback identifier that marks a registered handler property.
    callback_id = props.get('callback_id')
    serialized = []

    # Preserve property order while converting the registered handler to JS.
    for name, value in props.items():
        if name != 'callback_id' and value == callback_id:
            serialized.append(
                f'{json.dumps(name)}:()=>send('
                f'{{{json.dumps(callback_id)}:{{}},timestamp:Date.now()}})'
            )
        else:
            serialized.append(f'{json.dumps(name)}:{json.dumps(value)}')

    # Return the JavaScript object expression containing serialized properties.
    return '{' + ','.join(serialized) + '}'

# *** blueprints

# ** blueprint: build_streamlit_binding
def build_streamlit_binding(
        handler_builder: Callable[[str, Callable[[Any], Any]], Callable[[], Any]] = None,
    ) -> Callable[..., Any]:
    '''
    Build a Streamlit-facing binding for rendering and interacting with Frames.

    The binding declares the vendored component once and builds a callback
    registry for each independent render pass.

    :param handler_builder: Optional factory for zero-argument host handlers.
    :type handler_builder: Callable[[str, Callable[[Any], Any]], Callable[[], Any]]
    :return: A callable that mounts Frames in the declared Streamlit component.
    :rtype: Callable[..., Any]
    '''

    # Declare the vendored component bundle once for this binding.
    component = declare_component(
        'muiElements',
        path=get_streamlit_bundle_path(),
    )

    # Resolve the supplied host-handler factory or compose the default one.
    handler_builder = handler_builder or build_handler_builder()

    # Bind one frame to a fresh callback registry for each render pass.
    def binding(frame: Any, key: str = 'tiferet_elements') -> Any:
        '''
        Mount one Frame through the declared Streamlit component.

        :param frame: The frame to serialize and mount.
        :type frame: Any
        :param key: The Streamlit component key for the mounted frame.
        :type key: str
        :return: The declared component's render result.
        :rtype: Any
        '''

        # Register this frame's callbacks before serializing its element tree.
        callback_table = BuildCallbackTable().execute(frame=frame)

        # Decode host payloads and dispatch them through this render's registry.
        def dispatch(payload: Any) -> Any:
            '''Decode a host payload before dispatching it to a frame callback.'''

            payload = json.loads(payload) if isinstance(payload, str) else payload
            return DispatchCallback().execute(
                callback_table=callback_table,
                payload=payload,
            )

        # Build the host callback after its dispatch closure is available.
        on_change = handler_builder(key, dispatch)

        # Render the serialized frame with its scoped host callback handler.
        return component(
            js=wrap_js_with_material_icons_font(
                '[' + ','.join(
                    _serialize_element(element)
                    for element in frame.elements
                ) + ']'
            ),
            key=key,
            on_change=on_change,
        )

    # Return the configured Streamlit-facing Frame binding.
    return binding
