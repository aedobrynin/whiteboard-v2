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


class ICardController(abc.ABC):
    @abc.abstractmethod
    def edit_text(
        self,
        obj_id: internal.objects.interfaces.ObjectId,
        text: str
    ):
        pass
