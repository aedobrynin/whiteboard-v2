from typing import Type, TypeVar
import abc
import dataclasses
import uuid


class IBoardObject(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self) -> uuid.UUID:
        pass

    @abc.abstractmethod
    def serialize(self) -> dict:
        pass

    # TODO: return type annotation
    @staticmethod
    @abc.abstractmethod
    def from_serialized(data: dict):
        pass


# TODO: move to models
@dataclasses.dataclass
class Position:
    x: int
    y: int
    z: int


class IBoardObjectWithPosition(IBoardObject):
    @property
    @abc.abstractmethod
    def position(self) -> Position:
        pass

    @position.setter
    @abc.abstractmethod
    def position(self, pos: Position) -> None:
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
