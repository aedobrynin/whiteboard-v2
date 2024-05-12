from __future__ import annotations

from datetime import datetime

import internal.pub_sub.interfaces
from internal.objects import interfaces
from .common import field_names
from .object import BoardObject
from .. import events
from .. import types

_START_ID_FIELD = 'start_id'
_END_ID_FIELD = 'end_id'
_COLOR_FIELD = 'color'
_WIDTH_FIELD = 'width'
_CONNECTOR_TYPE_FIELD = 'connector_type'
_STROKE_STYLE_FIELD = 'stroke_style'
DEFAULT_CONNECTOR_TYPE = 'curved'
DEFAULT_STROKE_STYLE = 'last'
DEFAULT_WIDTH = 2
DEFAULT_COLOR = 'black'


class BoardObjectConnector(interfaces.IBoardObjectConnector, BoardObject):
    def __init__(
        self,
        id: interfaces.ObjectId,
        create_dttm: datetime,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        start_id: interfaces.ObjectId,
        end_id: interfaces.ObjectId,
        color: str = DEFAULT_COLOR,
        width: float = DEFAULT_WIDTH,
        connector_type: str = DEFAULT_CONNECTOR_TYPE,
        stroke_style: str = DEFAULT_STROKE_STYLE,
    ):
        BoardObject.__init__(
            self, id, types.BoardObjectType.CONNECTOR, create_dttm, pub_sub_broker
        )
        self.start_id = start_id
        self.end_id = end_id
        self.connector_type = connector_type
        self.stroke_style = stroke_style
        self.color = color
        self.width = width

    @property
    def start_id(self) -> interfaces.ObjectId:
        return self._start_id

    @start_id.setter
    def start_id(self, obj_id: interfaces.ObjectId) -> None:
        self._start_id = obj_id

    @property
    def end_id(self) -> interfaces.ObjectId:
        return self._end_id

    @end_id.setter
    def end_id(self, obj_id: interfaces.ObjectId) -> None:
        self._end_id = obj_id

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        self._color = color
        self._publish(events.EventObjectChangedColor(self.id))

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, width: float) -> None:
        self._width = width
        self._publish(events.EventObjectChangedWidth(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

    @property
    def connector_type(self) -> str:
        return self._connector_type

    @connector_type.setter
    def connector_type(self, connector_type: str) -> None:
        self._connector_type = connector_type
        self._publish(events.EventObjectChangedConnectorType(self.id))

    @property
    def stroke_style(self) -> str:
        return self._stroke_style

    @stroke_style.setter
    def stroke_style(self, stroke_style: str) -> None:
        self._stroke_style = stroke_style
        self._publish(events.EventObjectChangedStrokeStyle(self.id))

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_START_ID_FIELD] = self._start_id
        serialized[_END_ID_FIELD] = self._end_id
        serialized[_COLOR_FIELD] = self.color
        serialized[_WIDTH_FIELD] = self.width
        serialized[_CONNECTOR_TYPE_FIELD] = self.connector_type
        serialized[_STROKE_STYLE_FIELD] = self.stroke_style
        return serialized

    @staticmethod
    def from_serialized(
        data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
    ) -> BoardObjectConnector:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectConnector(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            pub_sub_broker,
            data[_START_ID_FIELD],
            data[_END_ID_FIELD],
            data[_COLOR_FIELD],
            data[_WIDTH_FIELD],
            data[_CONNECTOR_TYPE_FIELD],
            data[_STROKE_STYLE_FIELD]
        )
