from __future__ import annotations

from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_font import BoardObjectWithFont
from .common import field_names
from .. import types

_TEXT_FIELD = 'text'
_FONT_FIELD = 'font'


class BoardObjectText(interfaces.IBoardObjectText, BoardObjectWithFont):
    def __init__(
        self,
        id: interfaces.ObjectId,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font()
    ):
        super().__init__(id, types.BoardObjectType.TEXT, position, pub_sub_broker, text, font)

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectText:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectText(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            internal.models.Font.from_serialized(data[_FONT_FIELD])
        )
