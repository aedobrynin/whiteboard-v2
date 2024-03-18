from __future__ import annotations
import uuid

from internal.objects import interfaces
from .common import field_names


class BoardObject(interfaces.IBoardObject):
    def __init__(self, id: uuid.UUID, type: str):
        self._id = id
        self._type = type

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    def serialize(self) -> dict:
        return {field_names.ID_FIELD: str(self.id), field_names.TYPE_FIELD: self.type}

    @staticmethod
    def from_serialized(data: dict) -> BoardObject:
        return BoardObject(uuid.UUID(data[field_names.ID_FIELD]), data[field_names.TYPE_FIELD])
