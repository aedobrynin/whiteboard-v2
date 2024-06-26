from __future__ import annotations

from datetime import datetime
from typing import List

import internal.pub_sub.interfaces
from internal.models import Position
from internal.objects import interfaces
from .common import field_names
from .object import BoardObject
from .. import events
from .. import types

_POINTS_FIELD = 'points'
_COLOR_FIELD = 'color'
_WIDTH_FIELD = 'width'


class BoardObjectPen(interfaces.IBoardObjectPen, BoardObject):
    def __init__(
        self,
        id: interfaces.ObjectId,
        create_dttm: datetime,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        points: List[internal.models.Position],  # noqa
        color: str = interfaces.IBoardObjectPen.DEFAULT_COLOR,
        width: int = interfaces.IBoardObjectPen.DEFAULT_WIDTH,
    ):
        BoardObject.__init__(self, id, types.BoardObjectType.PEN, create_dttm, pub_sub_broker)
        self.points = points
        self.color = color
        self.width = width

    @property
    def points(self) -> List[internal.models.Position]:
        return self._points

    @points.setter
    def points(self, points: List[internal.models.Position]) -> None:
        self._points = points
        self._publish(events.EventObjectChangedPoints(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

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
        self._publish(events.EventObjectChangedWidth(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_POINTS_FIELD] = [p.serialize() for p in self.points]
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
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            pub_sub_broker,
            [Position.from_serialized(p) for p in data[_POINTS_FIELD]],
            data[_COLOR_FIELD],
            data[_WIDTH_FIELD],
        )
