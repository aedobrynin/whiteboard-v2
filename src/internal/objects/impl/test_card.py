import internal.pub_sub.mocks
from internal.models import Position, Font

from .card import BoardObjectCard
from .object_id import generate_object_id


def test_board_object_card_serialization():
    id = generate_object_id()
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    color = 'light blue'
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectCard(id, position, broker, text, font, color)
    assert card.serialize() == {
        'id': id,
        'position': position.serialize(),
        'text': text,
        'type': 'card',
        'font': font.serialize(),
        'color': color
    }


def test_board_object_card_deserialization():
    id = generate_object_id()
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    color = 'light blue'

    serialized = {
        'id': id,
        'position': position.serialize(),
        'text': text,
        'type': 'card',
        'font': font.serialize(),
        'color': color
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    board = BoardObjectCard.from_serialized(serialized, broker)
    assert board.id == id
    assert board.position == position
    assert board.text == text
    assert board.font == font
    assert board.color == color
