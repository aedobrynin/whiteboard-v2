import internal.pub_sub.mocks
from internal.models import Position

from .pen import BoardObjectPen
from ..types import BoardObjectType
from .object_id import generate_object_id


def test_board_pen_serialization():
    id = generate_object_id()
    type = BoardObjectType.PEN
    points = [Position(1, 2, 3), Position(2, 2, 3), Position(3, 2, 3)]
    color = 'black'
    width = 2.0
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectPen(id, broker, points, color, width)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'points': [p.serialize() for p in points],
        'color': color,
        'width': width
    }


def test_board_pen_deserialization():
    id = generate_object_id()
    type = BoardObjectType.PEN
    points = [Position(1, 2, 3), Position(2, 2, 3), Position(3, 2, 3)]
    color = 'black'
    width = 2.0

    serialized = {
        'id': id,
        'type': type.value,
        'points': [p.serialize() for p in points],
        'color': color,
        'width': width
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj: BoardObjectPen = BoardObjectPen.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.points == points
    assert obj.color == color
    assert obj.width == width
