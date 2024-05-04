from __future__ import annotations

from typing import List

from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_position import BoardObjectWithPosition
from .common import field_names
from .. import types

_TABLE_COLUMNS_FIELD = 'table-columns'
_TABLE_ROWS_FIELD = 'table-rows'
_COLUMNS_WIDTH = 'columns-width'
_ROWS_HEIGHT = 'rows-height'
_DEFAULT_WIDTH = 'default-width'
_DEFAULT_HEIGHT = 'default-height'


class BoardObjectTable(interfaces.IBoardObjectTable, BoardObjectWithPosition):
    def __init__(
            self,
            id: interfaces.ObjectId,
            position: internal.models.Position,
            pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
            columns: int = 2,
            rows: int = 2,
            width: float = 50,
            height: float = 30,
            col_widths: list[float] = None,
            row_heights: list[float] = None
    ):
        super().__init__(id, types.BoardObjectType.TABLE, position, pub_sub_broker)
        self.columns = columns
        self.rows = rows
        self.default_width = width
        self.default_height = height
        if col_widths is None:
            self.columns_width = [width] * columns
        else:
            self.columns_width = col_widths
        if col_widths is None:
            self.rows_height = [height] * rows
        else:
            self.rows_height = row_heights

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_TABLE_COLUMNS_FIELD] = self.columns
        serialized[_TABLE_ROWS_FIELD] = self.rows
        serialized[_DEFAULT_WIDTH] = self.default_width
        serialized[_DEFAULT_HEIGHT] = self.default_height

        serialized[_COLUMNS_WIDTH] = self.columns_width
        serialized[_ROWS_HEIGHT] = self.rows_height

        return serialized

    @staticmethod
    def from_serialized(
            data: dict,
            pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectTable:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectTable(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            int(data[_TABLE_COLUMNS_FIELD]),
            int(data[_TABLE_ROWS_FIELD]),
            data[_DEFAULT_WIDTH],
            data[_DEFAULT_HEIGHT],
            data[_COLUMNS_WIDTH],
            data[_ROWS_HEIGHT]

        )
    @property
    def default_width(self) -> float:
        return self._default_width

    @default_width.setter
    def default_width(self, val: float) -> None:
        self._default_width = val

    @property
    def default_height(self) -> float:
        return self._default_height

    @default_height.setter
    def default_height(self, val: float) -> None:
        self._default_height = val

    @property
    def columns(self) -> int:
        return self._columns

    @columns.setter
    def columns(self, val: int) -> None:
        self._columns = val

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, val: int) -> None:
        self._rows = val

    @property
    def columns_width(self) -> list:
        return self._columns_width

    @columns_width.setter
    def columns_width(self, val: list) -> None:
        self._columns_width = val

    @property
    def rows_height(self) -> list:
        return self._rows_height

    @rows_height.setter
    def rows_height(self, val: list) -> None:
        self._rows_height = val

    # @property
    # def props(self) -> List[str]:
    #     return [
    #             _TABLE_COLUMNS_FIELD,
    #             _TABLE_ROWS_FIELD,
    #             _DEFAULT_WIDTH,
    #             _DEFAULT_HEIGHT,
    #             _COLUMNS_WIDTH,
    #             _ROWS_HEIGHT
    #     ]

    def tags_object(self, coords):
        return f"cell~" + coords + f"/{self.id}"
