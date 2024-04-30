from __future__ import annotations
import abc
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

    @property
    @abc.abstractmethod
    def props(self) -> List[str]:
        pass


class IBoardObjectText(IBoardObjectWithPosition):
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
    def font_slant(self) -> str:
        pass

    @font_slant.setter
    @abc.abstractmethod
    def font_slant(self, font_slant: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def font_weight(self) -> str:
        pass

    @font_weight.setter
    @abc.abstractmethod
    def font_weight(self, font_weight: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def font_color(self) -> str:
        pass

    @font_color.setter
    @abc.abstractmethod
    def font_color(self, font_color: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def font_family(self) -> str:
        pass

    @font_family.setter
    @abc.abstractmethod
    def font_family(self, font_family: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def font_size(self) -> float:
        pass

    @font_size.setter
    @abc.abstractmethod
    def font_size(self, font_size: float) -> None:
        pass


class IBoardObjectCard(IBoardObjectWithPosition):
    @property
    @abc.abstractmethod
    def text(self) -> str:
        pass

    @text.setter
    @abc.abstractmethod
    def text(self, text: str) -> None:
        pass
