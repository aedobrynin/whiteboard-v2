from __future__ import annotations
from datetime import datetime
from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_position import BoardObjectWithPosition
from .common import field_names
from .. import events
from .. import types

_TABLE_COLUMNS_FIELD = 'table-columns'
_TABLE_ROWS_FIELD = 'table-rows'
_COLUMNS_WIDTH = 'columns-width'
_ROWS_HEIGHT = 'rows-height'
_DEFAULT_WIDTH = 'default-width'
_DEFAULT_HEIGHT = 'default-height'
_LINKED_OBJECTS = 'linked-objects'


class BoardObjectTable(interfaces.IBoardObjectTable, BoardObjectWithPosition):
    def __init__(
        self,
        id: interfaces.ObjectId,
        create_dttm: datetime,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        columns: int = 2,
        rows: int = 2,
        width: float = 50,
        height: float = 30,
        col_widths: list[float] = None,
        row_heights: list[float] = None,
        linked_objects: dict[str, list] = None,
    ):
        super().__init__(id, types.BoardObjectType.TABLE, create_dttm, position, pub_sub_broker)
        self.default_width = width
        self.default_height = height
        if col_widths is None:
            self.columns_width = [self.default_width] * columns
        else:
            self.columns_width = col_widths
        if row_heights is None:
            self.rows_height = [self.default_height] * rows
        else:
            self.rows_height = row_heights
        if linked_objects:
            self.linked_objects = linked_objects
        else:
            self.linked_objects = {}

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_TABLE_COLUMNS_FIELD] = self.columns
        serialized[_TABLE_ROWS_FIELD] = self.rows
        serialized[_DEFAULT_WIDTH] = self.default_width
        serialized[_DEFAULT_HEIGHT] = self.default_height
        serialized[_COLUMNS_WIDTH] = self.columns_width
        serialized[_ROWS_HEIGHT] = self.rows_height
        serialized[_LINKED_OBJECTS] = self.linked_objects
        return serialized

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectTable:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectTable(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            datetime.strptime(data[field_names.CREATE_DTTM_FIELD], '%Y-%m-%dT%H-%M-%SZ'),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            int(data[_TABLE_COLUMNS_FIELD]),
            int(data[_TABLE_ROWS_FIELD]),
            data[_DEFAULT_WIDTH],
            data[_DEFAULT_HEIGHT],
            data[_COLUMNS_WIDTH],
            data[_ROWS_HEIGHT],
            data[_LINKED_OBJECTS],
        )

    @property
    def default_width(self) -> float:
        return self._default_width

    @default_width.setter
    def default_width(self, default_width: float) -> None:
        self._default_width = default_width

    @property
    def default_height(self) -> float:
        return self._default_height

    @default_height.setter
    def default_height(self, default_height: float) -> None:
        self._default_height = default_height

    @property
    def columns(self) -> int:
        return len(self.columns_width)

    @property
    def rows(self) -> int:
        return len(self.rows_height)

    @property
    def columns_width(self) -> list:
        return self._columns_width

    @columns_width.setter
    def columns_width(self, columns_width: list) -> None:
        self._columns_width = columns_width
        self._publish(events.EventObjectChangedColumnSize(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

    @property
    def rows_height(self) -> list:
        return self._rows_height

    @rows_height.setter
    def rows_height(self, rows_height: list) -> None:
        self._rows_height = rows_height
        self._publish(events.EventObjectChangedRowSize(self.id))
        self._publish(events.EventObjectChangedSize(self.id))

    @property
    def linked_objects(self) -> dict[str, list]:
        return self._linked_objects

    @linked_objects.setter
    def linked_objects(self, objects: dict[str, list]) -> None:
        self._linked_objects = objects
        self._publish(events.EventObjectChangedLinkedObjects(self.id))
        self._publish(events.EventObjectChangedSize(self.id))
