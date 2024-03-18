from __future__ import annotations
import uuid

from internal.objects import interfaces
from .registered_types import board_object_type
import internal.models
from .object_with_position import BoardObjectWithPosition
from .common import field_names

_TEXT_FIELD = 'text'
_TYPE_NAME = 'card'


@board_object_type(_TYPE_NAME)
class BoardObjectCard(interfaces.IBoardObjectCard, BoardObjectWithPosition):
    def __init__(self, id: uuid.UUID, position: internal.models.Position, text: str):
        super().__init__(id, _TYPE_NAME, position)
        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_TEXT_FIELD] = self.text
        return serialized

    @staticmethod
    def from_serialized(data: dict) -> BoardObjectCard:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectCard(
            uuid.UUID(data[field_names.ID_FIELD]),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            data[_TEXT_FIELD],
        )
