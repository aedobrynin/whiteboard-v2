from __future__ import annotations

from internal.objects import interfaces
import internal.pub_sub.interfaces
from .common import field_names
from .object import BoardObject
from .. import types
from .. import events

_CHILDREN_IDS_FIELD = 'children_ids'


class BoardObjectGroup(interfaces.IBoardObjectGroup, BoardObject):
    def __init__(
        self,
        id: interfaces.ObjectId,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        children_ids: tuple[internal.objects.interfaces.ObjectId]
    ):
        BoardObject.__init__(
            self, id,
            types.BoardObjectType.GROUP,
            pub_sub_broker
        )
        self.children_ids = children_ids

    @property
    def children_ids(self) -> tuple[internal.objects.interfaces.ObjectId]:
        return self._children_ids

    @children_ids.setter
    def children_ids(
        self, children_ids: tuple[internal.objects.interfaces.ObjectId]
    ) -> None:
        self._children_ids = children_ids
        self._publish(events.EventObjectChangedSize(self.id))

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_CHILDREN_IDS_FIELD] = self.children_ids
        return serialized

    @staticmethod
    def from_serialized(
        data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
    ) -> BoardObjectGroup:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectGroup(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            pub_sub_broker,
            data[_CHILDREN_IDS_FIELD]
        )
