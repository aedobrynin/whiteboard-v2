from __future__ import annotations
import abc
from typing import List

from internal.objects import interfaces
from internal.models import Position
import internal.pub_sub.interfaces
from .common import field_names
from .object import BoardObject
from .. import types


class BoardObjectWithPosition(interfaces.IBoardObjectWithPosition, BoardObject, abc.ABC):
    def __init__(
        self,
        id: interfaces.ObjectId,
        type: types.BoardObjectType,  # noqa
        position: Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ):
        BoardObject.__init__(self, id, type, pub_sub_broker)
        self.position = position
        self.focus = False

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        self._position = position

    @property
    def focus(self) -> bool:
        return self._focus

    @focus.setter
    def focus(self, focus: bool) -> None:
        self._focus = focus

    @property
    def props(self) -> List[str]:
        return []

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[field_names.POSITION_FIELD] = self.position.serialize()
        return serialized

    @staticmethod
    def from_serialized(
        data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
    ) -> BoardObjectWithPosition:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectWithPosition(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            types.BoardObjectType(data[field_names.TYPE_FIELD]),
            Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
        )
