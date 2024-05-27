from datetime import datetime

import internal.pub_sub.mocks
from internal.models import Position
from .object_id import generate_object_id
from .table import BoardObjectTable
from ..types import BoardObjectType


def test_board_object_table_serialization():
    id = generate_object_id()
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    type = BoardObjectType.TABLE
    columns = 2
    rows = 2
    width = 50
    height = 30
    col_widths = [width] * columns
    row_heights = [height] * rows
    linked_objects = {}
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    table_object = BoardObjectTable(
        id,
        create_dttm,
        position,
        broker,
        columns,
        rows,
        width,
        height,
        col_widths,
        row_heights,
        linked_objects,
    )
    assert table_object.serialize() == {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'type': type.value,
        'position': position.serialize(),
        'table-columns': columns,
        'table-rows': rows,
        'columns-width': col_widths,
        'rows-height': row_heights,
        'default-width': width,
        'default-height': height,
        'linked-objects': linked_objects,
    }


def test_board_object_table_deserialization():
    id = generate_object_id()
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    type = BoardObjectType.TABLE
    columns = 2
    rows = 2
    width = 50
    height = 30
    col_widths = [width] * columns
    row_heights = [height] * rows
    linked_objects = {}

    serialized = {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'type': type.value,
        'position': position.serialize(),
        'table-columns': columns,
        'table-rows': rows,
        'columns-width': col_widths,
        'rows-height': row_heights,
        'default-width': width,
        'default-height': height,
        'linked-objects': linked_objects,
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    table_object = BoardObjectTable.from_serialized(serialized, broker)
    assert table_object.id == id
    assert table_object.type == type
    assert table_object.create_dttm == create_dttm
    assert table_object.position == position
    assert table_object.columns == columns
    assert table_object.rows == rows
    assert table_object.default_width == width
    assert table_object.default_height == height
    assert table_object.columns_width == col_widths
    assert table_object.rows_height == row_heights
