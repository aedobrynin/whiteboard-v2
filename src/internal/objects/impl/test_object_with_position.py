from datetime import datetime

import internal.pub_sub.mocks
from internal.models import Position
from .object_id import generate_object_id
from .object_with_position import BoardObjectWithPosition
from ..types import BoardObjectType


def test_board_object_with_position_serialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    position = Position(1, 2, 3)
    create_dttm = datetime.now().replace(microsecond=0)
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithPosition(id, type, create_dttm, position, broker)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ')
    }


def test_board_object_with_position_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    position = Position(1, 2, 3)
    create_dttm = datetime.now().replace(microsecond=0)

    serialized = {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ')
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithPosition.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.create_dttm == create_dttm
    assert obj.position == position
    assert obj.create_dttm == obj.create_dttm
