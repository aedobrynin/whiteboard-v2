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


class IBoardObjectPen(IBoardObject):

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


class IBoardObjectGroup(IBoardObject):

    @property
    @abc.abstractmethod
    def children_ids(self) -> tuple[ObjectId]:
        pass

    @children_ids.setter
    @abc.abstractmethod
    def children_ids(self, children_ids: tuple[ObjectId]) -> None:
        pass


class IBoardObjectConnector(IBoardObject):

    @property
    @abc.abstractmethod
    def start_id(self) -> ObjectId:
        pass

    @start_id.setter
    @abc.abstractmethod
    def start_id(self, obj_id: ObjectId) -> None:
        pass

    @property
    @abc.abstractmethod
    def end_id(self) -> ObjectId:
        pass

    @end_id.setter
    @abc.abstractmethod
    def end_id(self, obj_id: ObjectId) -> None:
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

    @property
    @abc.abstractmethod
    def connector_type(self) -> str:
        pass

    @connector_type.setter
    @abc.abstractmethod
    def connector_type(self, connector_type: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def stroke_style(self) -> str:
        pass

    @stroke_style.setter
    @abc.abstractmethod
    def stroke_style(self, stroke_style: str) -> None:
        pass
