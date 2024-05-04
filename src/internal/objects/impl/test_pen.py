import internal.pub_sub.mocks
from internal.models import Position

from .pen import BoardObjectPen
from ..types import BoardObjectType
from .object_id import generate_object_id


def test_board_object_with_font_serialization():
    id = generate_object_id()
    type = BoardObjectType.PEN
    position = Position(1, 2, 3)
    points = [Position(1, 2, 3), Position(2, 2, 3), Position(3, 2, 3)]
    color = 'black'
    width = 2.0
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectPen(id, type, position, broker, points, color, width)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
        'points': points,
        'color': color,
        'width': width
    }


def test_board_object_with_font_deserialization():
    id = generate_object_id()
    type = BoardObjectType.PEN
    position = Position(1, 2, 3)
    points = [Position(1, 2, 3), Position(2, 2, 3), Position(3, 2, 3)]
    color = 'black'
    width = 2.0

    serialized = {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
        'points': points,
        'color': color,
        'width': width
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj: BoardObjectPen = BoardObjectPen.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.position == position
    assert obj.points == points
    assert obj.color == color
    assert obj.width == width
