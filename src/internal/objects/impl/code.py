from __future__ import annotations

from datetime import datetime

from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_font import BoardObjectWithFont
from .common import field_names
from .. import types
from .. import events

_TEXT_FIELD = 'text'
_FONT_FIELD = 'font'
_LEXER_FIELD = 'lexer'


class BoardObjectCode(interfaces.IBoardObjectCode, BoardObjectWithFont):
    def __init__(
        self,
        id: interfaces.ObjectId,
        create_dttm: datetime,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'print(2 + 2)',
        font: internal.models.Font = internal.models.Font(),
        lexer: str = 'python',
    ):
        super().__init__(id, types.BoardObjectType.CODE, create_dttm, position, pub_sub_broker,
                         text, font)
        self.lexer = lexer

    @property
    def lexer(self) -> str:
        return self._lexer

    @lexer.setter
    def lexer(self, lexer: str) -> None:
        self._lexer = lexer
        self._publish(events.EventObjectChangedLexer(self.id))

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_LEXER_FIELD] = self.lexer
        return serialized

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectCode:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectCode(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            internal.models.Font.from_serialized(data[_FONT_FIELD]),
            data[_LEXER_FIELD],
        )
