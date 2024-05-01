from __future__ import annotations

from internal.objects import interfaces
from internal.models import Position, Font
import internal.pub_sub.interfaces
from .common import field_names
from .object_with_position import BoardObjectWithPosition
from .. import types
from .. import events

_TEXT_FIELD = 'text'
_FONT_FIELD = 'font'


class BoardObjectWithFont(interfaces.IBoardObjectWithFont, BoardObjectWithPosition):
    def __init__(
        self,
        id: interfaces.ObjectId,
        type: types.BoardObjectType,  # noqa
        position: Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font()
    ):
        BoardObjectWithPosition.__init__(self, id, type, position, pub_sub_broker)
        self._text = text
        self._font = font  # to escape calling setter pub-sub event

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    @property
    def font(self) -> internal.models.Font:
        return self._font

    @font.setter
    def font(self, font: internal.models.Font) -> None:
        self._font = font
        self._publish(events.EventObjectChangedSize(self.id))

    def update_font(self, **kwargs):
        self.font.update_fields(**kwargs)
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
            Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            Font.from_serialized(data[_FONT_FIELD])
        )
