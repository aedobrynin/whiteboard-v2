from typing import List

_FONT_MIN_SIZE = 8
_FONT_MAX_SIZE = 64
_FONT_STEP = 1


def get_font_slants() -> List[str]:
    return ['roman', 'italic']


def get_font_weights() -> List[str]:
    return ['normal', 'bold']


def get_font_sizes() -> List[int]:
    return list(range(_FONT_MIN_SIZE, _FONT_MAX_SIZE, _FONT_STEP))


def get_font_colors() -> List[str]:
    return [
        'gray',
        'light yellow',
        'yellow',
        'orange',
        'light green',
        'green',
        'dark green',
        'cyan',
        'light pink',
        'pink',
        'violet',
        'red',
        'light blue',
        'dark blue',
        'black',
    ]


def get_text_alignments() -> List[str]:
    return ['left', 'center', 'right']


def get_line_widths() -> List[int]:
    return [1, 2, 3, 4, 5]


def get_line_types() -> List[str]:
    return ['solid', 'dotted', 'dashed']


def get_connector_types() -> List[str]:
    return ['elbowed', 'straight', 'curved']


def get_stroke_styles() -> List[str]:
    return ['first', 'both', 'last', 'none']


def get_card_sizes() -> List[str]:
    return ['Small', 'Medium', 'Large']


def get_font_families() -> List[str]:
    return [
        'Arial',
        'Calibri',
        'Cambria',
        'Century',
        'Consolas',
        'Corbel',
        'Courier',
        'Dubai',
        'Georgia',
        'Impact',
        'Mistral',
        'Modern',
        'Montserrat',
        'Papyrus',
        'Pristina',
        'Roman',
        'Script',
        'SimSun',
        'Symbol',
        'Tahoma',
        'Terminal',
        'Verdana',
        'Wingdings',
    ]
