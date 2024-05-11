from __future__ import annotations
import abc
from typing import List

import internal.models
import internal.objects
import internal.objects.interfaces


class IController(abc.ABC):
    @abc.abstractmethod
    def create_object(self, type: internal.objects.BoardObjectType, **kwargs):
        pass

    @abc.abstractmethod
    def delete_object(self, obj_id: internal.objects.interfaces.ObjectId):
        pass

    @abc.abstractmethod
    def edit_text(self, obj_id: internal.objects.interfaces.ObjectId, text: str):
        pass

    @abc.abstractmethod
    def edit_font(self, obj_id: internal.objects.interfaces.ObjectId, font: internal.models.Font):
        pass

    @abc.abstractmethod
    def edit_color(self, obj_id: internal.objects.interfaces.ObjectId, color: str):
        pass

    @abc.abstractmethod
    def edit_width(self, obj_id: internal.objects.interfaces.ObjectId, width: float):
        pass

    @abc.abstractmethod
    def edit_dimension(
        self, obj_id: internal.objects.interfaces.ObjectId, dimension: float
    ):
        pass

    @abc.abstractmethod
    def edit_points(
        self, obj_id: internal.objects.interfaces.ObjectId, points: List[internal.models.Position]
    ):
        pass

    @abc.abstractmethod
    def move_object(
        self, obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position
    ):
        pass

    @abc.abstractmethod
    def undo_last_action(self):
        pass

    @abc.abstractmethod
    def redo_last_action(self):
        pass
