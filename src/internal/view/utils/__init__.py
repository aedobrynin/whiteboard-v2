from . import geometry as geometry
from .font import as_tkinter_font, as_object_font, as_tkinter_object_font
from .props_values import (
    get_font_slants,
    get_font_weights,
    get_font_sizes,
    get_font_colors,
    get_font_families,
    get_text_alignments,
    get_line_widths,
    get_line_types,
    get_connector_types,
    get_stroke_styles
)

__all__ = [
    'as_tkinter_font',
    'as_tkinter_object_font',
    'as_object_font',
    'get_font_slants',
    'get_font_weights',
    'get_font_sizes',
    'get_font_colors',
    'get_font_families',
    'get_text_alignments',
    'get_line_widths',
    'get_line_types',
    'get_connector_types',
    'get_stroke_styles',
    'geometry'
]
