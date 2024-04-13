import internal.pub_sub.mocks

from .object import BoardObject
from ..types import BoardObjectType
from .object_id import generate_object_id


def test_board_object_serialization():
    id = generate_object_id()
    type = BoardObjectType.CARD

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObject(id, type, broker)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
    }


def test_board_object_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CARD.value

    serialized = {
        'id': id,
        'type': type,
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObject.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == BoardObjectType.CARD
