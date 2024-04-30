from .canvas_repo_obj import (
    get_current,
    get_current_opt_type,
    get_current_opt
)
from .props_values import (
    get_font_slant,
    get_font_weight,
    get_font_size,
    get_font_colors,
    get_font_family,
    get_text_alignment,
    get_text_line_width,
    get_line_type
)

from . import geometry as geometry

from .object_border import (
    draw_border,
    remove_border
)

__all__ = [
    'get_current',
    'get_current_opt_type',
    'get_current_opt',
    'get_font_slant',
    'get_font_weight',
    'get_font_size',
    'get_font_colors',
    'get_font_family',
    'get_text_alignment',
    'get_text_line_width',
    'get_line_type',
    'geometry',
    'draw_border',
    'remove_border'
]
