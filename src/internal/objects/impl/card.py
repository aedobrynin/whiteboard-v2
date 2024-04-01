from __future__ import annotations

from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_position import BoardObjectWithPosition
from .common import field_names
from .. import types

_TEXT_FIELD = 'text'


class BoardObjectCard(interfaces.IBoardObjectCard, BoardObjectWithPosition):
    def __init__(
        self,
        id: interfaces.ObjectId,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
    ):
        super().__init__(id, types.BoardObjectType.card, position, pub_sub_broker)
        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_TEXT_FIELD] = self.text
        return serialized

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectCard:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectCard(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
        )
