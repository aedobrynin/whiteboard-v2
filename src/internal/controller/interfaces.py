from __future__ import annotations

import abc
import typing

import internal.models
import internal.objects
import internal.objects.interfaces


class IController(abc.ABC):
    @abc.abstractmethod
    def create_object(self, type: internal.objects.BoardObjectType, **kwargs):
        pass

    @abc.abstractmethod
    def create_object_from_repr(self, obj_repr: dict):
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
    def edit_width(self, obj_id: internal.objects.interfaces.ObjectId, width: int):
        pass

    @abc.abstractmethod
    def edit_height(self, obj_id: internal.objects.interfaces.ObjectId, height: int):
        pass

    @abc.abstractmethod
    def edit_size(self, obj_id: internal.objects.interfaces.ObjectId, width: int, height: int):
        pass

    @abc.abstractmethod
    def edit_points(
        self,
        obj_id: internal.objects.interfaces.ObjectId,
        points: typing.List[internal.models.Position],
    ):
        pass

    @abc.abstractmethod
    def edit_children_ids(
        self,
        obj_id: internal.objects.interfaces.ObjectId,
        children_ids: typing.List[str],
    ):
        pass

    @abc.abstractmethod
    def move_object(
        self, obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position
    ):
        pass

    @abc.abstractmethod
    def edit_connector_type(
        self, obj_id: internal.objects.interfaces.ObjectId, connector_type: str
    ):
        pass

    @abc.abstractmethod
    def edit_stroke_style(self, obj_id: internal.objects.interfaces.ObjectId, stroke_style: str):
        pass

    def edit_table(self, obj_id: internal.objects.interfaces.ObjectId, list_col, list_row):
        pass

    def edit_linked_objects(
        self, obj_id: internal.objects.interfaces.ObjectId, linked_obj: typing.Dict[str, list[int]]
    ):
        pass

    def undo_last_action(self):
        pass

    @abc.abstractmethod
    def redo_last_action(self):
        pass
