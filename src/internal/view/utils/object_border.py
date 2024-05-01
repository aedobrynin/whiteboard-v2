import logging

import internal.objects.interfaces
import internal.view.dependencies
from .geometry import Rectangle

_OFFSET = 3


def _get_frame_border(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId
) -> Rectangle:
    obj_frame = list(dependencies.canvas.bbox(obj_id))
    obj_frame[0] -= _OFFSET
    obj_frame[1] -= _OFFSET
    obj_frame[2] += _OFFSET
    obj_frame[3] += _OFFSET
    return internal.view.utils.geometry.Rectangle.from_tkinter_rect(tuple(obj_frame))


def _is_border_drawn(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId
):
    return bool(dependencies.canvas.gettags(obj_id))


def draw_border(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId
):
    COLOR = 'black'
    REC_WIDTH = 2
    rect = _get_frame_border(dependencies, obj_id)
    obj_id = f'rectangle{obj_id}'
    if _is_border_drawn(dependencies, obj_id):
        dependencies.canvas.coords(obj_id, *rect.as_tkinter_rect())
    else:
        dependencies.canvas.create_rectangle(
            *rect.as_tkinter_rect(), outline=COLOR, width=REC_WIDTH, tags=obj_id
        )


def remove_border(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId
):
    obj_id = f'rectangle{obj_id}'
    dependencies.canvas.delete(obj_id)
