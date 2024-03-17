from __future__ import annotations
import uuid

from .interfaces import IBoardObjectCard, Position


class BoardObjectCard(IBoardObjectCard):
    def __init__(self, id: uuid.UUID, position: Position, text: str):
        # TODO: try to move such usual fields into separate helper class
        self._id = id
        self._position = position
        self._text = text

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, pos: Position) -> None:
        self._position = pos

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    def serialize(self) -> dict:
        return {
            'id': str(self.id),
            'position': {
                'x': self.position.x,
                'y': self.position.y,
                'z': self.position.z,
            },
            'text': self.text,
        }

    @staticmethod
    def from_serialized(data: dict) -> BoardObjectCard:
        return BoardObjectCard(
            uuid.UUID(data['id']),
            Position(data['position']['x'], data['position']['y'], data['position']['z']),
            data['text'],
        )
