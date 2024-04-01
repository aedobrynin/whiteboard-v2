import uuid

from .object import BoardObject
from ..types import BoardObjectType
import internal.pub_sub.mocks


def test_board_object_serialization():
    _id = uuid.uuid4()
    _type = BoardObjectType.card

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObject(_id, _type, broker)
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

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObject.from_serialized(serialized, broker)
    assert obj.id == _id
    assert obj.type == BoardObjectType.card
