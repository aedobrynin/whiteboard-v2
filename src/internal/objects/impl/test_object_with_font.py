from datetime import datetime

import internal.pub_sub.mocks
from internal.models import Position, Font
from .object_id import generate_object_id
from .object_with_font import BoardObjectWithFont
from ..types import BoardObjectType


def test_board_object_with_font_serialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithFont(id, type, create_dttm, position, broker, text, font)
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': position.serialize(),
        'text': text,
        'font': font.serialize()
    }


def test_board_object_with_font_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()

    serialized = {
        'id': id,
        'type': type.value,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': position.serialize(),
        'text': text,
        'font': font.serialize()
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectWithFont.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.create_dttm == create_dttm
    assert obj.position == position
    assert obj.text == text
    assert obj.font == font
