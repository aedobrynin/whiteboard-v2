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
_COLOR_FIELD = 'color'
_WIDTH_FIELD = 'width'
_HEIGHT_FIELD = 'height'
_ATTRIBUTED_FIELD = 'attribute'


class BoardObjectCard(interfaces.IBoardObjectCard, BoardObjectWithFont):

    def __init__(
        self,
        id: interfaces.ObjectId,
        create_dttm: datetime,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font(),
        color: str = 'light yellow',
        width: int = 150,
        height: int = 150,
        attribute: dict[str, str] = dict(),  # noqa
    ):
        super().__init__(id, types.BoardObjectType.CARD, create_dttm, position, pub_sub_broker, text, font)
        self.color = color
        self.width = width
        self.height = height
        self.attribute = attribute

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        self._color = color
        self._publish(events.EventObjectChangedColor(self.id))

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        self._width = width
        self._publish(events.EventObjectChangedSize(self.id))

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        self._height = height
        self._publish(events.EventObjectChangedSize(self.id))

    @property
    def attribute(self) -> int:
        return self._attribute

    @attribute.setter
    def attribute(self, attribute: dict[str, str]) -> None:
        self._attribute = attribute

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_COLOR_FIELD] = self.color
        serialized[_WIDTH_FIELD] = self.width
        serialized[_HEIGHT_FIELD] = self.height
        serialized[_ATTRIBUTED_FIELD] = self.attribute
        return serialized

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectCard:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectCard(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            internal.models.Font.from_serialized(data[_FONT_FIELD]),
            data[_COLOR_FIELD],
            data[_WIDTH_FIELD],
            data[_HEIGHT_FIELD],
            data[_ATTRIBUTED_FIELD],
        )
