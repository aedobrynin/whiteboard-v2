from __future__ import annotations

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
_DIMENSION_FIELD = 'dimension'


class BoardObjectCard(interfaces.IBoardObjectCard, BoardObjectWithFont):
    def __init__(
        self,
        id: interfaces.ObjectId,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font: internal.models.Font = internal.models.Font(),
        color: str = 'light yellow',
        dimension: int = [150, 150],
    ):
        super().__init__(id, types.BoardObjectType.CARD, position, pub_sub_broker, text, font)
        self.color = color
        self.dimension = dimension

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        self._color = color
        self._publish(events.EventObjectChangedColor(self.id))

    @property
    def dimension(self) -> [int, int]:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: [int, int]) -> None:
        self._dimension = dimension
        self._publish(events.EventObjectChangedDimension(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_COLOR_FIELD] = self.color
        serialized[_DIMENSION_FIELD] = self.dimension
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
            data[_COLOR_FIELD],
            data[_DIMENSION_FIELD],
        )
