import uuid

from .object_with_position import BoardObjectWithPosition
from internal.models import Position


def test_board_object_with_position_serialization():
    _id = uuid.uuid4()
    _type = 'type'
    position = Position(1, 2, 3)

    obj = BoardObjectWithPosition(_id, _type, position)
    assert obj.serialize() == {
        'id': str(_id),
        'type': _type,
        'position': position.serialize(),
    }


def test_board_object_with_position_deserialization():
    _id = uuid.uuid4()
    _type = 'type'
    position = Position(1, 2, 3)

    serialized = {
        'id': str(_id),
        'type': _type,
        'position': position.serialize(),
    }

    obj = BoardObjectWithPosition.from_serialized(serialized)
    assert obj.id == _id
    assert obj.type == _type
    assert obj.position == position