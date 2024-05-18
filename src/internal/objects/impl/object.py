from __future__ import annotations

from datetime import datetime

import internal.pub_sub.interfaces
from .common import field_names
from .. import interfaces
from .. import types


class BoardObject(interfaces.IBoardObject):
    # TODO: think about a better place for pubsubbroker
    def __init__(
        self,
        id: interfaces.ObjectId,  # type: ignore
        type: types.BoardObjectType,  # type: ignore
        create_dttm: datetime,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ):
        self._id = id
        self._type = type
        self._pub_sub_broker = pub_sub_broker
        self._create_dttm = create_dttm

    @property
    def id(self) -> interfaces.ObjectId:
        return self._id

    @property
    def type(self) -> types.BoardObjectType:
        return self._type

    @property
    def create_dttm(self) -> datetime:
        return self._create_dttm

    def serialize(self) -> dict:
        return {
            field_names.ID_FIELD: self.id,
            field_names.TYPE_FIELD: self.type.value,
            field_names.CREATE_DTTM_FIELD: self.create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ')
        }

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObject:
        return BoardObject(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            types.BoardObjectType(data[field_names.TYPE_FIELD]),
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            pub_sub_broker,
        )

    def _publish(self, event: internal.pub_sub.interfaces.Event):
        self._pub_sub_broker.publish(self.id, event)
