from __future__ import annotations

from internal.objects import interfaces
from internal.models import Position
from .common import field_names
from .object import BoardObject


class BoardObjectWithPosition(interfaces.IBoardObjectWithPosition, BoardObject):
    def __init__(self, id: interfaces.ObjectId, type: str, position: Position):
        BoardObject.__init__(self, id, type)
        self.position = position

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        self._position = position

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[field_names.POSITION_FIELD] = self.position.serialize()
        return serialized

    @staticmethod
    def from_serialized(data: dict) -> BoardObjectWithPosition:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectWithPosition(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            data[field_names.TYPE_FIELD],
            Position.from_serialized(data[field_names.POSITION_FIELD]),
        )
