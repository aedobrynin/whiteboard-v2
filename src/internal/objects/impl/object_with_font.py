from __future__ import annotations

from datetime import datetime

import internal.pub_sub.interfaces
from internal.models import Position, Font
from internal.objects import interfaces
from .common import field_names
from .object_with_position import BoardObjectWithPosition
from .. import events
from .. import types

_TEXT_FIELD = 'text'
_FONT_FIELD = 'font'


class BoardObjectWithFont(interfaces.IBoardObjectWithFont, BoardObjectWithPosition):
    def __init__(
        self,
        id: interfaces.ObjectId,
        type: types.BoardObjectType,  # noqa
        create_dttm: datetime,
        position: Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font()
    ):
        BoardObjectWithPosition.__init__(self, id, type, create_dttm, position, pub_sub_broker)
        self.text = text
        self.font = font

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self._publish(events.EventObjectChangedText(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

    @property
    def font(self) -> internal.models.Font:
        return self._font

    @font.setter
    def font(self, font: internal.models.Font) -> None:
        self._font = font
        self._publish(events.EventObjectChangedFont(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_TEXT_FIELD] = self.text
        serialized[_FONT_FIELD] = self.font.serialize()
        return serialized

    @staticmethod
    def from_serialized(
        data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
    ) -> BoardObjectWithFont:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectWithFont(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            types.BoardObjectType(data[field_names.TYPE_FIELD]),
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            Font.from_serialized(data[_FONT_FIELD])
        )
