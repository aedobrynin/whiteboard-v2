from __future__ import annotations

import internal.pub_sub.interfaces

from .. import interfaces
from .common import field_names
from .. import types


class BoardObject(interfaces.IBoardObject):
    # TODO: think about a better place for pubsubbroker
    def __init__(
        self,
        id: interfaces.ObjectId,
        type: types.BoardObjectType,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ):
        self._id = id
        self._type = type
        self._pub_sub_broker = pub_sub_broker

    @property
    def id(self) -> interfaces.ObjectId:
        return self._id

    @property
    def type(self) -> types.BoardObjectType:
        return self._type

    def serialize(self) -> dict:
        return {field_names.ID_FIELD: str(self.id), field_names.TYPE_FIELD: self.type.value}

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObject:
        return BoardObject(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            types.BoardObjectType(data[field_names.TYPE_FIELD]),
            pub_sub_broker,
        )

    def _publish(self, event: internal.pub_sub.interfaces.Event):
        self._pub_sub_broker.publish(str(self.id), event)
