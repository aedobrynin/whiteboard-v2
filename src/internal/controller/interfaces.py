from __future__ import annotations
import abc

import internal.models
import internal.objects
import internal.objects.interfaces


class IController(abc.ABC):
    @abc.abstractmethod
    def create_object(
        self, type: internal.objects.BoardObjectType, position: internal.models.Position
    ):
        pass

    @abc.abstractmethod
    def delete_object(
        self, obj_id: internal.objects.interfaces.ObjectId
    ):
        pass

    @abc.abstractmethod
    def edit_text(
        self, obj_id: internal.objects.interfaces.ObjectId, text: str
    ):
        pass

    @abc.abstractmethod
    def edit_font(
        self, obj_id: internal.objects.interfaces.ObjectId, **kwargs
    ):
        pass

    @abc.abstractmethod
    def edit_card_color(
        self, obj_id: internal.objects.interfaces.ObjectId, color: str
    ):
        pass

    @abc.abstractmethod
    def move_object(
        self, obj_id: internal.objects.interfaces.ObjectId, position: internal.models.Position
    ):
        pass

    @abc.abstractmethod
    def edit_focus(
        self, obj_id: internal.objects.interfaces.ObjectId, focus: bool
    ):
        pass
