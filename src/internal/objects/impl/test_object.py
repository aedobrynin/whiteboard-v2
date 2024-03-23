import uuid

from .object import BoardObject
from ..types import BoardObjectType


def test_board_object_serialization():
    _id = uuid.uuid4()
    _type = BoardObjectType.card

    obj = BoardObject(_id, _type)
    assert obj.serialize() == {
        'id': str(_id),
        'type': _type.value,
    }


def test_board_object_deserialization():
    _id = uuid.uuid4()
    _type = BoardObjectType.card.value

    serialized = {
        'id': str(_id),
        'type': _type,
    }

    obj = BoardObject.from_serialized(serialized)
    assert obj.id == _id
    assert obj.type == BoardObjectType.card
