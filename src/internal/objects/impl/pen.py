from __future__ import annotations

from typing import List

from internal.objects import interfaces
from internal.models import Position, Font
import internal.pub_sub.interfaces
from .common import field_names
from .object_with_position import BoardObjectWithPosition
from .. import types
from .. import events

_POINT_FIELD = 'points'
_COLOR_FIELD = 'color'
_WIDTH_FIELD = 'width'


class BoardObjectPen(interfaces.IBoardObjectPen, BoardObjectWithPosition):
    def __init__(
        self,
        id: interfaces.ObjectId,
        position: Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        points: List[internal.models.Position] = [Position(0, 0, 0)],  # noqa
        color: str = 'black',
        width: float = 2
    ):
        BoardObjectWithPosition.__init__(
            self, id,
            types.BoardObjectType.PEN,
            position,
            pub_sub_broker
        )
        self._points = points
        self._color = color  # to escape calling setter pub-sub event
        self._width = width

    @property
    def points(self) -> List[internal.models.Position]:
        return self._points

    @points.setter
    def points(self, points: List[internal.models.Position]) -> None:
        self._points = points
        self._publish(events.EventObjectChangedSize(self.id))

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        self._color = color

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, width: float) -> None:
        self._width = width
        self._publish(events.EventObjectChangedSize(self.id))

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_POINT_FIELD] = [p.serialize() for p in self.points]
        serialized[_COLOR_FIELD] = self.color
        serialized[_WIDTH_FIELD] = self.width
        return serialized

    @staticmethod
    def from_serialized(
        data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
    ) -> BoardObjectPen:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectPen(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            [Position.from_serialized(p) for p in data[_POINT_FIELD]],
            data[_COLOR_FIELD],
            data[_WIDTH_FIELD]
        )