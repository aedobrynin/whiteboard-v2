from __future__ import annotations
import abc
from abc import ABC
from typing import List

import internal.models
import internal.pub_sub.interfaces
from . import types

# TODO: class ObjectId with methods for serialization and creation
ObjectId = str


class IBoardObject(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self) -> ObjectId:
        pass

    # TODO: myb hide type from here
    @property
    @abc.abstractmethod
    def type(self) -> types.BoardObjectType:
        pass

    # TODO typedef SerializedObject = dict
    @abc.abstractmethod
    def serialize(self) -> dict:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_serialized(
        data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
    ) -> IBoardObject:
        pass


class IBoardObjectWithPosition(IBoardObject):
    @property
    @abc.abstractmethod
    def position(self) -> internal.models.Position:
        pass

    @position.setter
    @abc.abstractmethod
    def position(self, pos: internal.models.Position) -> None:
        pass

    @property
    @abc.abstractmethod
    def focus(self) -> bool:
        pass

    @focus.setter
    @abc.abstractmethod
    def focus(self, focus: bool) -> None:
        pass


class IBoardObjectWithFont(IBoardObjectWithPosition):
    @property
    @abc.abstractmethod
    def text(self) -> str:
        pass

    @text.setter
    @abc.abstractmethod
    def text(self, text: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def font(self) -> internal.models.Font:
        pass

    @font.setter
    @abc.abstractmethod
    def font(self, font: internal.models.Font) -> None:
        pass

    @abc.abstractmethod
    def update_font(self, **kwargs):
        pass


class IBoardObjectText(IBoardObjectWithFont, ABC):
    pass


class IBoardObjectCard(IBoardObjectWithFont):
    @property
    @abc.abstractmethod
    def color(self) -> str:
        pass

    @color.setter
    @abc.abstractmethod
    def color(self, color: str) -> None:
        pass


class IBoardObjectPen(IBoardObjectWithPosition):

    @property
    @abc.abstractmethod
    def points(self) -> List[internal.models.Position]:
        pass

    @points.setter
    @abc.abstractmethod
    def points(self, points: List[internal.models.Position]) -> None:
        pass

    @property
    @abc.abstractmethod
    def color(self) -> str:
        pass

    @color.setter
    @abc.abstractmethod
    def color(self, color: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def width(self) -> float:
        pass

    @width.setter
    @abc.abstractmethod
    def width(self, width: float) -> None:
        pass

class IBoardObjectTable(IBoardObjectWithPosition):
    @property
    @abc.abstractmethod
    def default_width(self) -> float:
        pass

    @default_width.setter
    @abc.abstractmethod
    def default_width(self, val: float) -> None:
        pass

    @property
    @abc.abstractmethod
    def default_height(self) -> float:
        pass

    @default_height.setter
    @abc.abstractmethod
    def default_height(self, val: float) -> None:
        pass

    @property
    @abc.abstractmethod
    def columns(self) -> int:
        pass

    @columns.setter
    @abc.abstractmethod
    def columns(self, val: int) -> None:
        pass

    @property
    @abc.abstractmethod
    def rows(self) -> int:
        pass

    @rows.setter
    @abc.abstractmethod
    def rows(self, val: int) -> None:
        pass

    @property
    @abc.abstractmethod
    def columns_width(self) -> list:
        pass

    @columns_width.setter
    @abc.abstractmethod
    def columns_width(self, val: list) -> None:
        pass

    @property
    @abc.abstractmethod
    def rows_height(self) -> list:
        pass

    @rows_height.setter
    @abc.abstractmethod
    def rows_height(self, val: list) -> None:
        pass

    @property
    @abc.abstractmethod
    def linked_objects(self) -> dict[str, [int, int]]:
        pass

    @linked_objects.setter
    @abc.abstractmethod
    def linked_objects(self, val: dict[str, [int, int]]) -> None:
        pass