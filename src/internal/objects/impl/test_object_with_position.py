import internal.pub_sub.mocks
from internal.models import Position

from .object_with_position import BoardObjectWithPosition
from ..types import BoardObjectType
from .object_id import generate_object_id


def test_board_object_with_position_serialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    position = Position(1, 2, 3)

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithPosition(id, type, position, broker)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
    }


def test_board_object_with_position_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    position = Position(1, 2, 3)

    serialized = {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithPosition.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.position == position
