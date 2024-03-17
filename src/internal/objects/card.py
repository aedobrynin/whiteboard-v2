from __future__ import annotations
import uuid

from . import interfaces
import internal.models
from .common import field_names

_TEXT_FIELD = 'text'


class BoardObjectCard(interfaces.IBoardObjectCard):
    def __init__(self, id: uuid.UUID, position: internal.models.Position, text: str):
        self._id = id
        self._position = position
        self._text = text

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def position(self) -> internal.models.Position:
        return self._position

    @position.setter
    def position(self, position: internal.models.Position) -> None:
        self._position = position

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    def serialize(self) -> dict:
        return {
            field_names.ID_FIELD: str(self.id),
            field_names.POSITION_FIELD: self.position.serialize(),
            _TEXT_FIELD: self.text,
        }

    @staticmethod
    def from_serialized(data: dict) -> BoardObjectCard:
        return BoardObjectCard(
            uuid.UUID(data[field_names.ID_FIELD]),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            data[_TEXT_FIELD],
        )
