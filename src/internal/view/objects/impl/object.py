from __future__ import annotations

from abc import ABC

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.utils.geometry

from ..interfaces import IViewObject

_RECTANGLE_PREFIX = 'rectangle'


class ViewObject(IViewObject, ABC):

    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObject
    ):
        self._id = obj.id
        self._is_focused = False

    @property
    def id(self):
        return self._id

    def set_focused(
        self, dependencies: internal.view.dependencies.Dependencies, is_focus: bool
    ):
        # myb, there will be notifications
        self._is_focused = is_focus

    def get_focused(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        # myb, there will be notifications
        return self._is_focused

    def move(
        self, dependencies: internal.view.dependencies.Dependencies, delta_x: int, delta_y: int
    ):
        dependencies.canvas.move(self.id, delta_x, delta_y)

    def move_to(
        self, dependencies: internal.view.dependencies.Dependencies, x: int, y: int
    ):
        dependencies.canvas.coords(self.id, x, y)

    def get_border_rectangle(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> internal.view.utils.geometry.Rectangle:
        OFFSET = 3
        obj_frame = list(dependencies.canvas.bbox(self.id))
        obj_frame[0] -= OFFSET
        obj_frame[1] -= OFFSET
        obj_frame[2] += OFFSET
        obj_frame[3] += OFFSET
        return internal.view.utils.geometry.Rectangle.from_tkinter_rect(tuple(obj_frame))

    def _is_border_drawn(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> bool:
        obj_id = f'{_RECTANGLE_PREFIX}{self.id}'
        return bool(dependencies.canvas.gettags(obj_id))

    def draw_object_border(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        COLOR = 'black'
        REC_WIDTH = 2
        rect = self.get_border_rectangle(dependencies)
        obj_id = f'{_RECTANGLE_PREFIX}{self.id}'
        if self._is_border_drawn(dependencies):
            dependencies.canvas.coords(obj_id, *rect.as_tkinter_rect())
        else:
            dependencies.canvas.create_rectangle(
                *rect.as_tkinter_rect(), outline=COLOR, width=REC_WIDTH, tags=obj_id
            )

    def remove_object_border(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        obj_id = f'{_RECTANGLE_PREFIX}{self.id}'
        dependencies.canvas.delete(obj_id)

    def destroy(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.canvas.delete(self.id)
