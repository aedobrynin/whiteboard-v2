from __future__ import annotations

from datetime import datetime

import internal.models
import internal.pub_sub.interfaces
from internal.objects import interfaces
from .common import field_names
from .object_with_font import BoardObjectWithFont
from .. import types

_TEXT_FIELD = 'text'
_FONT_FIELD = 'font'


class BoardObjectText(interfaces.IBoardObjectText, BoardObjectWithFont):
    def __init__(
        self,
        id: interfaces.ObjectId,
        create_dttm: datetime,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font()
    ):
        super().__init__(id, types.BoardObjectType.TEXT, create_dttm, position, pub_sub_broker, text, font)

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectText:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectText(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            internal.models.Font.from_serialized(data[_FONT_FIELD])
        )
