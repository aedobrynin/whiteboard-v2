from __future__ import annotations

from datetime import datetime

import internal.pub_sub.interfaces
from internal.models import Position
from internal.objects import interfaces
from .common import field_names
from .object import BoardObject
from .. import events
from .. import types


class BoardObjectWithPosition(interfaces.IBoardObjectWithPosition, BoardObject):
    def __init__(
        self,
        id: interfaces.ObjectId,
        type: types.BoardObjectType,  # noqa
        create_dttm: datetime,
        position: Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
    ):
        BoardObject.__init__(self, id, type, create_dttm, pub_sub_broker)
        self.position = position

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
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
        )
