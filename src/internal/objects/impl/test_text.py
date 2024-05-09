import internal.pub_sub.mocks
from internal.models import Position, Font

from .text import BoardObjectText
from .object_id import generate_object_id
from ..types import BoardObjectType


def test_board_object_text_serialization():
    id = generate_object_id()
    position = Position(1, 2, 3)
    text = 'text'
    type = BoardObjectType.TEXT
    font = Font()
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    tex_object = BoardObjectText(id, position, broker, text, font)
    assert tex_object.serialize() == {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
        'text': text,
        'font': font.serialize()
    }


def test_board_object_text_deserialization():
    id = generate_object_id()
    type = BoardObjectType.TEXT
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()

    serialized = {
        'id': id,
        'type': type.value,
        'position': position.serialize(),
        'text': text,
        'font': font.serialize()
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    text_object = BoardObjectText.from_serialized(serialized, broker)
    assert text_object.id == id
    assert text_object.type == type
    assert text_object.text == text
    assert text_object.font == font
