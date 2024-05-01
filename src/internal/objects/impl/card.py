from __future__ import annotations

from typing import List

from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_font import BoardObjectWithFont
from .common import field_names
from .. import types

_TEXT_FIELD = 'text'
_FONT_FIELD = 'font'
_CARD_COLOR_FIELD = 'card_color'


class BoardObjectCard(interfaces.IBoardObjectCard, BoardObjectWithFont):
    def __init__(
        self,
        id: interfaces.ObjectId,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font(),
        card_color: str = 'light yellow'
    ):
        super().__init__(id, types.BoardObjectType.CARD, position, pub_sub_broker, text, font)
        self._card_color = card_color

    @property
    def card_color(self) -> str:
        return self._card_color

    @card_color.setter
    def card_color(self, color: str) -> None:
        self._card_color = color

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_CARD_COLOR_FIELD] = self.card_color
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
            internal.models.Font.from_serialized(data[_FONT_FIELD]),
            data[_CARD_COLOR_FIELD]
        )
