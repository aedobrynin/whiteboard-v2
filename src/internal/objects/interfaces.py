import abc
import uuid

import internal.models


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

    # TODO: return type annotation
    @staticmethod
    @abc.abstractmethod
    def from_serialized(data: dict):
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
