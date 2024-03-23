from __future__ import annotations

from internal.objects import interfaces
from .common import field_names

from .. import types


class BoardObject(interfaces.IBoardObject):
    def __init__(self, id: interfaces.ObjectId, type: types.BoardObjectType):
        self._id = id
        self._type = type

    @property
    def id(self) -> interfaces.ObjectId:
        return self._id

    @property
    def type(self) -> types.BoardObjectType:
        return self._type

    def serialize(self) -> dict:
        return {field_names.ID_FIELD: str(self.id), field_names.TYPE_FIELD: self.type.value}

    @staticmethod
    def from_serialized(data: dict) -> BoardObject:
        return BoardObject(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            types.BoardObjectType(data[field_names.TYPE_FIELD]),
        )
