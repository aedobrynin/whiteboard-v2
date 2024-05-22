from datetime import datetime

import internal.pub_sub.mocks
from .group import BoardObjectGroup
from .object_id import generate_object_id
from ..types import BoardObjectType


def test_board_group_serialization():
    id = generate_object_id()
    type = BoardObjectType.GROUP
    create_dttm = datetime.now().replace(microsecond=0)
    children_ids = (generate_object_id(), generate_object_id())
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectGroup(id, create_dttm, broker, children_ids)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'children_ids': children_ids
    }


def test_board_group_deserialization():
    id = generate_object_id()
    type = BoardObjectType.GROUP
    create_dttm = datetime.now().replace(microsecond=0)
    children_ids = (generate_object_id(), generate_object_id())
    serialized = {
        'id': id,
        'type': type.value,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'children_ids': children_ids
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj: BoardObjectGroup = BoardObjectGroup.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.children_ids == children_ids
    assert obj.create_dttm == create_dttm
