from __future__ import annotations

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.utils.geometry

from ..interfaces import IViewObject

_RECTANGLE_PREFIX = 'rectangle'
_ALIGNING_PREFIX = 'aligning'


class ViewObject(IViewObject):
    def __init__(
        self,
        obj: internal.objects.interfaces.IBoardObject,
    ):
        self._id = obj.id
        self._is_focused = False

    @property
    def id(self):
        return self._id

    def set_focused(self, dependencies: internal.view.dependencies.Dependencies, is_focus: bool):
        # myb, there will be notifications
        self._is_focused = is_focus

    def get_focused(self, dependencies: internal.view.dependencies.Dependencies):
        # myb, there will be notifications
        return self._is_focused

    def move_to(self, dependencies: internal.view.dependencies.Dependencies, x: float, y: float):
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

    def _is_border_drawn(self, dependencies: internal.view.dependencies.Dependencies) -> bool:
        obj_id = f'{_RECTANGLE_PREFIX}{self.id}'
        return bool(dependencies.canvas.gettags(obj_id))

    def draw_object_border(self, dependencies: internal.view.dependencies.Dependencies):
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

    def remove_object_border(self, dependencies: internal.view.dependencies.Dependencies):
        obj_id = f'{_RECTANGLE_PREFIX}{self.id}'
        dependencies.canvas.delete(obj_id)

    def _is_aligning_line_drawn(self, dependencies: internal.view.dependencies.Dependencies):
        obj_id = f'{_ALIGNING_PREFIX}{self.id}'
        return bool(dependencies.canvas.gettags(obj_id))

    def _update_aligning_line(
        self, points: list[int], dependencies: internal.view.dependencies.Dependencies
    ):
        COLOR = 'blue'
        obj_id = f'{_ALIGNING_PREFIX}{self.id}'
        if self._is_aligning_line_drawn(dependencies):
            dependencies.canvas.coords(obj_id, *points)
        else:
            dependencies.canvas.create_line(*points, fill=COLOR, tags=obj_id)

    def aligning(self, dependencies: internal.view.dependencies.Dependencies):
        obj_frame = list(dependencies.canvas.bbox(self.id))
        _PADDING = 5 * max(obj_frame[3] - obj_frame[1], obj_frame[2] - obj_frame[0])
        # flag = False

        top = dependencies.canvas.find_overlapping(
            obj_frame[0] - _PADDING, obj_frame[1] - _PADDING, obj_frame[2] + _PADDING, obj_frame[1]
        )
        for item in top:
            tags = dependencies.canvas.gettags(item)
            # TODO: connector and group exclusion
            if tags[0] == self.id or tags[0] in dependencies.canvas.gettags(self.id):
                continue

            obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
            if not (
                obj_x1 in [obj_frame[0], obj_frame[2]] or obj_x2 in [obj_frame[0], obj_frame[2]]
            ):
                continue

            if obj_frame[0] == obj_x1:
                points = [obj_x1, obj_y1, obj_frame[0], obj_frame[3]]
                self._update_aligning_line(points, dependencies)
                return
            if obj_frame[0] == obj_x2:
                points = [obj_x2, obj_y1, obj_frame[0], obj_frame[3]]
                self._update_aligning_line(points, dependencies)
                return
            if obj_frame[2] == obj_x1:
                points = [obj_x1, obj_y1, obj_frame[2], obj_frame[3]]
                self._update_aligning_line(points, dependencies)
                return
            if obj_frame[2] == obj_x2:
                points = [obj_x2, obj_y1, obj_frame[2], obj_frame[3]]
                self._update_aligning_line(points, dependencies)
                return
            self.remove_aligning(dependencies)
        else:
            bottom = dependencies.canvas.find_overlapping(
                obj_frame[0] - _PADDING,
                obj_frame[3],
                obj_frame[2] + _PADDING,
                obj_frame[3] + _PADDING,
            )
            for item in bottom:
                tags = dependencies.canvas.gettags(item)
                # TODO: connector and group exclusion
                if tags[0] == self.id or tags[0] in dependencies.canvas.gettags(self.id):
                    continue
                obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
                if not (
                    obj_x1 in [obj_frame[0], obj_frame[2]] or obj_x2 in [obj_frame[0], obj_frame[2]]
                ):
                    continue

                if obj_frame[0] == obj_x1:
                    points = [obj_frame[0], obj_frame[3], obj_x1, obj_y1]
                    self._update_aligning_line(points, dependencies)
                    return
                if obj_frame[0] == obj_x2:
                    points = [obj_frame[0], obj_frame[3], obj_x2, obj_y1]
                    self._update_aligning_line(points, dependencies)
                    return
                if obj_frame[2] == obj_x1:
                    points = [obj_frame[2], obj_frame[3], obj_x1, obj_y1]
                    self._update_aligning_line(points, dependencies)
                    return
                if obj_frame[2] == obj_x2:
                    points = [obj_frame[2], obj_frame[3], obj_x2, obj_y1]
                    self._update_aligning_line(points, dependencies)
                    return
                self.remove_aligning(dependencies)
        left = dependencies.canvas.find_overlapping(
            obj_frame[0] - _PADDING, obj_frame[1] - _PADDING, obj_frame[0], obj_frame[3] + _PADDING
        )
        for item in left:
            tags = dependencies.canvas.gettags(item)
            # TODO: connector and group exclusion
            if tags[0] == self.id or tags[0] in dependencies.canvas.gettags(self.id):
                continue
            obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
            if not (
                obj_y1 in [obj_frame[1], obj_frame[3]] or obj_y2 in [obj_frame[1], obj_frame[3]]
            ):
                continue

            if obj_frame[1] == obj_y1:
                points = [obj_x1, obj_y1, obj_frame[2], obj_frame[1]]
                self._update_aligning_line(points, dependencies)
                return
            if obj_frame[1] == obj_y2:
                points = [obj_x1, obj_y2, obj_frame[2], obj_frame[1]]
                self._update_aligning_line(points, dependencies)
                return
            if obj_frame[3] == obj_y1:
                points = [obj_x1, obj_y1, obj_frame[2], obj_frame[3]]
                self._update_aligning_line(points, dependencies)
                return
            if obj_frame[3] == obj_y2:
                points = [obj_x1, obj_y2, obj_frame[2], obj_frame[3]]
                self._update_aligning_line(points, dependencies)
                return
            self.remove_aligning(dependencies)
        else:
            right = dependencies.canvas.find_overlapping(
                obj_frame[2],
                obj_frame[1] - _PADDING,
                obj_frame[2] + _PADDING,
                obj_frame[3] + _PADDING,
            )
            for item in right:
                tags = dependencies.canvas.gettags(item)
                # TODO: connector and group exclusion
                if tags[0] == self.id or tags[0] in dependencies.canvas.gettags(self.id):
                    continue
                obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
                if not (
                    obj_y1 in [obj_frame[1], obj_frame[3]] or obj_y2 in [obj_frame[1], obj_frame[3]]
                ):
                    continue

                if obj_frame[1] == obj_y1:
                    points = [obj_frame[2], obj_frame[1], obj_x1, obj_y1]
                    self._update_aligning_line(points, dependencies)
                    return
                if obj_frame[1] == obj_y2:
                    points = [obj_frame[2], obj_frame[1], obj_x1, obj_y2]
                    self._update_aligning_line(points, dependencies)
                    return
                if obj_frame[3] == obj_y1:
                    points = [obj_frame[2], obj_frame[3], obj_x1, obj_y1]
                    self._update_aligning_line(points, dependencies)
                    return
                if obj_frame[3] == obj_y2:
                    points = [obj_frame[2], obj_frame[3], obj_x1, obj_y2]
                    self._update_aligning_line(points, dependencies)
                    return
            self.remove_aligning(dependencies)

    def scale(self, dependencies: internal.view.dependencies.Dependencies):
        pass

    def remove_aligning(self, dependencies: internal.view.dependencies.Dependencies):
        obj_id = f'{_ALIGNING_PREFIX}{self.id}'
        dependencies.canvas.delete(obj_id)

    def destroy(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.canvas.delete(self.id)
