"""Tiferet Elements Core Assets."""

# *** imports

# ** app
from tiferet.assets.core import (
    EN_US,
    create_default_error_data,
    create_service_module_path,
)

# *** constants (ids)

# ** constant: state_service_id
STATE_SERVICE_ID = 'state_service'

# ** constant: callback_not_found_id
CALLBACK_NOT_FOUND_ID = 'CALLBACK_NOT_FOUND'

# ** constant: widget_type_not_found_id
WIDGET_TYPE_NOT_FOUND_ID = 'WIDGET_TYPE_NOT_FOUND'

# *** constants (models)

# ** constant: callback_not_found_data
CALLBACK_NOT_FOUND_DATA = create_default_error_data(
    'Callback Not Found',
    [
        (
            EN_US,
            'No handler registered for callback_id {callback_id}.',
        ),
    ],
)

# ** constant: widget_type_not_found_data
WIDGET_TYPE_NOT_FOUND_DATA = create_default_error_data(
    'Widget Type Not Found',
    [
        (
            EN_US,
            'No Element defaults are registered for widget type {widget_type}.',
        ),
    ],
)

# *** constants (registrations)

# ** constant: state_service_registration_data
STATE_SERVICE_REGISTRATION_DATA = {
    'dependencies': [
        {
            'flag': 'streamlit',
            'module_path': create_service_module_path(
                'tiferet_elements',
                'utils',
                'streamlit',
            ),
            'class_name': 'StreamlitState',
            'parameters': {},
        },
    ],
}

# *** constants (widgets)

# ** constant: button_element_defaults
BUTTON_ELEMENT_DEFAULTS = {
    'type': 'Button',
    'props': {
        'variant': 'contained',
    },
}

# ** constant: text_field_element_defaults
TEXT_FIELD_ELEMENT_DEFAULTS = {
    'type': 'TextField',
    'props': {
        'variant': 'outlined',
    },
}

# ** constant: box_element_defaults
BOX_ELEMENT_DEFAULTS = {
    'type': 'Box',
    'props': {
        'component': 'div',
        'sx': {
            'border': '1px solid',
            'borderColor': 'divider',
            'borderRadius': 1,
            'p': 2,
        },
    },
}

# ** constant: icon_element_defaults
ICON_ELEMENT_DEFAULTS = {
    'type': 'Icon',
    'props': {},
}

# ** constant: card_element_defaults
CARD_ELEMENT_DEFAULTS = {
    'type': 'Card',
    'props': {
        'sx': {
            'p': 2,
        },
        'variant': 'outlined',
    },
}

# ** constant: form_label_element_defaults
FORM_LABEL_ELEMENT_DEFAULTS = {
    'type': 'FormLabel',
    'props': {},
}

# ** constant: typography_element_defaults
TYPOGRAPHY_ELEMENT_DEFAULTS = {
    'type': 'Typography',
    'props': {
        'variant': 'h6',
    },
}

# ** constant: widget_element_defaults
WIDGET_ELEMENT_DEFAULTS = {
    'button': BUTTON_ELEMENT_DEFAULTS,
    'text_field': TEXT_FIELD_ELEMENT_DEFAULTS,
    'box': BOX_ELEMENT_DEFAULTS,
    'icon': ICON_ELEMENT_DEFAULTS,
    'card': CARD_ELEMENT_DEFAULTS,
    'form_label': FORM_LABEL_ELEMENT_DEFAULTS,
    'typography': TYPOGRAPHY_ELEMENT_DEFAULTS,
}
