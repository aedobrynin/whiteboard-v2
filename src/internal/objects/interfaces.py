from __future__ import annotations
import abc
import uuid

import internal.models

# TODO: typedef ObjectId = uuid.UUID


class IBoardObject(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self) -> uuid.UUID:
        pass

    # TODO: myb hide type from here
    @property
    @abc.abstractmethod
    def type(self) -> str:
        pass

    @abc.abstractmethod
    def serialize(self) -> dict:
        pass

    @staticmethod
    @abc.abstractmethod
    def from_serialized(data: dict) -> IBoardObject:
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
