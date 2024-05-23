from datetime import datetime

import internal.pub_sub.mocks
from internal.models import Position
from .object_id import generate_object_id
from .pen import BoardObjectPen
from ..types import BoardObjectType


def test_board_pen_serialization():
    id = generate_object_id()
    type = BoardObjectType.PEN
    create_dttm = datetime.now().replace(microsecond=0)
    points = [Position(1, 2, 3), Position(2, 2, 3), Position(3, 2, 3)]
    color = 'black'
    width = 2
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectPen(id, create_dttm, broker, points, color, width)
    assert obj.serialize() == {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'type': type.value,
        'points': [p.serialize() for p in points],
        'color': color,
        'width': width
    }


def test_board_pen_deserialization():
    id = generate_object_id()
    type = BoardObjectType.PEN
    create_dttm = datetime.now().replace(microsecond=0)
    points = [Position(1, 2, 3), Position(2, 2, 3), Position(3, 2, 3)]
    color = 'black'
    width = 2

    serialized = {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'type': type.value,
        'points': [p.serialize() for p in points],
        'color': color,
        'width': width
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj: BoardObjectPen = BoardObjectPen.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.create_dttm == create_dttm
    assert obj.points == points
    assert obj.color == color
    assert obj.width == width
