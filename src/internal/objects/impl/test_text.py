from datetime import datetime

import internal.pub_sub.mocks
from internal.models import Position, Font
from .object_id import generate_object_id
from .text import BoardObjectText
from ..types import BoardObjectType


def test_board_object_text_serialization():
    id = generate_object_id()
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    text = 'text'
    type = BoardObjectType.TEXT
    font = Font()
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    tex_object = BoardObjectText(id, create_dttm, position, broker, text, font)
    assert tex_object.serialize() == {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'type': type.value,
        'position': position.serialize(),
        'text': text,
        'font': font.serialize()
    }


def test_board_object_text_deserialization():
    id = generate_object_id()
    create_dttm = datetime.now().replace(microsecond=0)
    type = BoardObjectType.TEXT
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

    text_object = BoardObjectText.from_serialized(serialized, broker)
    assert text_object.id == id
    assert text_object.type == type
    assert text_object.create_dttm == create_dttm
    assert text_object.text == text
    assert text_object.font == font
