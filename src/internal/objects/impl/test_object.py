from datetime import datetime

import internal.pub_sub.mocks
from .object import BoardObject
from .object_id import generate_object_id
from ..types import BoardObjectType


def test_board_object_serialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    create_dttm = datetime.now().replace(microsecond=0)
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObject(id, type, create_dttm, broker)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ')
    }


def test_board_object_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CARD.value
    create_dttm = datetime.now().replace(microsecond=0)

    serialized = {
        'id': id,
        'type': type,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ')
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObject.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == BoardObjectType.CARD
    assert obj.create_dttm == create_dttm
