from __future__ import annotations

import abc
import datetime
from abc import ABC
import typing

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

    @property
    @abc.abstractmethod
    def create_dttm(self) -> datetime.datetime:
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

    @property
    @abc.abstractmethod
    def width(self) -> int:
        pass

    @width.setter
    @abc.abstractmethod
    def width(self, width: int) -> None:
        pass

    @property
    @abc.abstractmethod
    def height(self) -> int:
        pass

    @height.setter
    @abc.abstractmethod
    def height(self, height: int) -> None:
        pass

    @property
    @abc.abstractmethod
    def attribute(self) -> dict[str, str]:
        pass

    @attribute.setter
    @abc.abstractmethod
    def attribute(self, attribute: dict[str, str]) -> None:
        pass


class IBoardObjectPen(IBoardObject):
    DEFAULT_WIDTH = 2
    DEFAULT_COLOR = 'black'

    @property
    @abc.abstractmethod
    def points(self) -> typing.List[internal.models.Position]:
        pass

    @points.setter
    @abc.abstractmethod
    def points(self, points: typing.List[internal.models.Position]) -> None:
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
    def width(self) -> int:
        pass

    @width.setter
    @abc.abstractmethod
    def width(self, width: int) -> None:
        pass


class IBoardObjectGroup(IBoardObject):
    @property
    @abc.abstractmethod
    def children_ids(self) -> typing.List[ObjectId]:
        pass

    @children_ids.setter
    @abc.abstractmethod
    def children_ids(self, children_ids: typing.List[ObjectId]) -> None:
        pass


class IBoardObjectConnector(IBoardObject):
    DEFAULT_WIDTH = 2
    DEFAULT_COLOR = 'black'
    DEFAULT_CONNECTOR_TYPE = 'curved'
    DEFAULT_STROKE_STYLE = 'last'

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

    @property
    @abc.abstractmethod
    def rows(self) -> int:
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
    def linked_objects(self) -> dict[str, list]:
        pass

    @linked_objects.setter
    @abc.abstractmethod
    def linked_objects(self, val: dict[str, list]) -> None:
        pass
