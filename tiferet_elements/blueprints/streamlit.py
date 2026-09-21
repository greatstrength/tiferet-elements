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
    '''
    Serialize one Element to the vendored bundle's render expression.

    :param element: The element whose props and children are rendered.
    :type element: Any
    :return: The JavaScript render expression for the element.
    :rtype: str
    '''

    # Serialize descendant elements before embedding their render expressions.
    children = ','.join(_serialize_element(child) for child in element.children)

    # Serialize props, replacing registered callback IDs with frontend senders.
    props = _serialize_props(element.props)

    # Render through the bundle's confirmed Material UI module key.
    return (
        f'render("muiElements",{json.dumps(element.type)},'
        f'{props},[{children}])'
    )

# ** function: _serialize_props
def _serialize_props(props: dict[str, Any]) -> str:
    '''
    Serialize Element props while restoring frontend event callbacks.

    :param props: The JSON-safe props created for the current render pass.
    :type props: dict[str, Any]
    :return: The JavaScript object expression for the element props.
    :rtype: str
    '''

    # Read the callback registration assigned by BuildCallbackTable, if present.
    callback_id = props.get('callback_id')
    serialized = []
    for name, value in props.items():

        # Replace the event prop's callback ID with the bundle's report sender.
        if name != 'callback_id' and value == callback_id:
            serialized.append(
                f'{json.dumps(name)}:()=>send({{{json.dumps(callback_id)}:{{}},'
                'timestamp:Date.now()})',
            )
            continue

        # Preserve ordinary JSON-compatible props without frontend transformation.
        serialized.append(f'{json.dumps(name)}:{json.dumps(value)}')

    # Return the frontend-ready JavaScript props object.
    return '{' + ','.join(serialized) + '}'

# *** blueprints

# ** blueprint: build_streamlit_binding
def build_streamlit_binding(
        handler_builder: Callable[[str, Callable[[Any], Any]], Callable[[], Any]] = None,
    ) -> Callable[..., Any]:
    '''
    Build the plain callable that mounts a Frame into a Streamlit session.

    The binding creates a fresh callback table per render pass and registers
    one public Streamlit ``on_change`` callback for reported interactions.

    :param handler_builder: Optional state-backed callback builder.
    :type handler_builder: Callable[[str, Callable[[Any], Any]], Callable[[], Any]] | None
    :return: A callable that mounts a Frame and dispatches its reports.
    :rtype: Callable[..., Any]
    '''

    # Declare the vendored component through Streamlit's supported public API.
    component = declare_component(
        'muiElements',
        path=get_streamlit_bundle_path(),
    )

    # Resolve the default Streamlit state-backed callback builder when omitted.
    handler_builder = handler_builder if handler_builder is not None else build_handler_builder()

    # Build the consumer-facing binding without constructing a session context.
    def binding(frame, key: str = 'tiferet_elements') -> Any:
        '''
        Mount one composed Frame and register its interaction dispatcher.

        :param frame: The frame to serialize and render.
        :type frame: Frame
        :param key: The stable Streamlit component key for this mounted frame.
        :type key: str
        :return: The component's current value.
        :rtype: Any
        '''

        # Build this render pass's frozen callback table before serialization.
        callback_table = BuildCallbackTable().execute(frame=frame)

        # Dispatch a reported payload against this render pass's registrations.
        def dispatch(payload: Any) -> Any:
            '''Dispatch one host-reported payload through the domain event.'''
            # Decode the vendored component's JSON session-state representation.
            payload = json.loads(payload) if isinstance(payload, str) else payload

            # Invoke the domain dispatcher directly with the captured snapshot.
            return DispatchCallback().execute(
                callback_table=callback_table,
                payload=payload,
            )

        # Build the public zero-argument on-change callback for this component.
        on_change = handler_builder(key, dispatch)

        # Serialize the frame, then inject Material Icons inside the iframe.
        return component(
            js=wrap_js_with_material_icons_font(
                '[' + ','.join(
                    _serialize_element(element)
                    for element in frame.elements
                ) + ']',
            ),
            key=key,
            on_change=on_change,
        )

    # Return the plain Binding callable to the host application.
    return binding
