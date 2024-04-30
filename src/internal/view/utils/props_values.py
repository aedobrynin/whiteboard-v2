from typing import List

_FONT_MIN_SIZE = 8
_FONT_MAX_SIZE = 65
_FONT_STEP = 2


def get_font_slant() -> List[str]:
    return ['roman', 'italic']


def get_font_weight() -> List[str]:
    return ['normal', 'bold']


def get_font_size() -> List[int]:
    return list(range(_FONT_MIN_SIZE, _FONT_MAX_SIZE, _FONT_STEP))


def get_font_colors() -> List[str]:
    return [
        'gray', 'light yellow', 'yellow', 'orange',
        'light green', 'green', 'dark green', 'cyan',
        'light pink', 'pink', 'pink', 'violet',
        'red', 'light blue', 'dark blue', 'black'
    ]


def get_text_alignment() -> List[str]:
    return ['left', 'center', 'right']


def get_text_line_width() -> List[int]:
    return [1, 2, 3, 4, 5]


def get_line_type() -> List[str]:
    return ['solid', 'dotted', 'dashed']


def get_font_family() -> List[str]:
    return [
        'Arial', 'Calibri', 'Cambria', 'Century',
        'Consolas', 'Corbel', 'Courier', 'Dubai',
        'Georgia', 'Impact', 'Mistral', 'Modern',
        'Montserrat', 'Papyrus', 'Pristina', 'Roman',
        'Script', 'SimSun', 'Symbol', 'Tahoma',
        'Terminal', 'Verdana', 'Wingdings'
    ]