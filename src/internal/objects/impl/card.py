from __future__ import annotations

from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_font import BoardObjectWithFont
from .common import field_names
from .. import types

_TEXT_FIELD = 'text'
_FONT_FIELD = 'font'
_COLOR_FIELD = 'color'
_ATTRIBUTES_FIELD = 'attributes_dict'

class BoardObjectCard(interfaces.IBoardObjectCard, BoardObjectWithFont):
    def __init__(
        self,
        id: interfaces.ObjectId,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font(),
        color: str = 'light yellow',
        attributes: dict = None
    ):
        super().__init__(id, types.BoardObjectType.CARD, position, pub_sub_broker, text, font)
        self._color = color
        if attributes is None:
            self.attributes = dict()
        else:
            self.attributes = attributes
    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        self._color = color

    @property
    def attributes(self) -> dict:
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: dict) -> None:
        self._attributes = attributes


    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_COLOR_FIELD] = self.color
        serialized[_ATTRIBUTES_FIELD] = list(map(lambda x: [x[0], x[1]], self.attributes.items()))
        return serialized

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectCard:
        temp = dict()
        for key, value in data[_ATTRIBUTES_FIELD]:
            temp[key] = value

        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectCard(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            internal.models.Font.from_serialized(data[_FONT_FIELD]),
            data[_COLOR_FIELD],
            temp
        )
