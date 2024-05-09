from __future__ import annotations

from internal.objects import interfaces
from internal.models import Position
import internal.pub_sub.interfaces
from .common import field_names
from .object import BoardObject
from .. import types
from .. import events


class BoardObjectWithPosition(interfaces.IBoardObjectWithPosition, BoardObject):
    def __init__(
        self,
        id: interfaces.ObjectId,
        type: types.BoardObjectType,  # noqa
        position: Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ):
        BoardObject.__init__(self, id, type, pub_sub_broker)
        self._position = position  # to escape calling setter pub-sub event

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        self._position = position
        self._publish(events.EventObjectMoved(self.id))

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
