from __future__ import annotations
import abc

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


class IBoardObjectCard(IBoardObjectWithPosition):
    @property
    @abc.abstractmethod
    def text(self) -> str:
        pass

    @text.setter
    @abc.abstractmethod
    def text(self, text: str) -> None:
        pass
