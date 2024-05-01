import internal.pub_sub.mocks
from internal.models import Position, Font

from .text import BoardObjectText
from .object_id import generate_object_id


def test_board_object_text_serialization():
    id = generate_object_id()
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectText(id, position, broker, text, font)
    assert card.serialize() == {
        'id': id,
        'position': position.serialize(),
        'text': text,
        'type': 'text',
        'font': font.serialize()
    }


def test_board_object_text_deserialization():
    id = generate_object_id()
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()

    serialized = {
        'id': id,
        'position': position.serialize(),
        'text': text,
        'type': 'card',
        'font': font.serialize()
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    board = BoardObjectText.from_serialized(serialized, broker)
    assert board.id == id
    assert board.position == position
    assert board.text == text
    assert board.font == font
