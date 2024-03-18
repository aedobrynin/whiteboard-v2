import uuid

from .object import BoardObject


def test_board_object_serialization():
    _id = uuid.uuid4()
    _type = 'type'

    obj = BoardObject(_id, _type)
    assert obj.serialize() == {
        'id': str(_id),
        'type': _type,
    }


def test_board_object_deserialization():
    _id = uuid.uuid4()
    _type = 'type'

    serialized = {
        'id': str(_id),
        'type': _type,
    }

    obj = BoardObject.from_serialized(serialized)
    assert obj.id == _id
    assert obj.type == _type
