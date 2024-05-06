from .canvas_repo_obj import (
    get_current,
    get_current_opt_type,
    get_current_opt
)
from .props_values import (
    get_font_slants,
    get_font_weights,
    get_font_sizes,
    get_font_colors,
    get_font_families,
    get_text_alignments,
    get_text_line_widths,
    get_line_types
)

from . import geometry as geometry

from .object_border import (
    draw_border,
    remove_border
)
from .object_aligning import (
    aligning,
    remove_aligning
)

__all__ = [
    'get_current',
    'get_current_opt_type',
    'get_current_opt',
    'get_font_slants',
    'get_font_weights',
    'get_font_sizes',
    'get_font_colors',
    'get_font_families',
    'get_text_alignments',
    'get_text_line_widths',
    'get_line_types',
    'geometry',
    'draw_border',
    'remove_border',
    'aligning',
    'remove_aligning'
]
