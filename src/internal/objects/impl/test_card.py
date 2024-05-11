import internal.pub_sub.mocks
from internal.models import Position, Font

from .card import BoardObjectCard
from .object_id import generate_object_id
from ..types import BoardObjectType


def test_board_object_card_serialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    color = 'light blue'
    dimension = [130, 130]
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectCard(id, position, broker, text, font, color, dimension)
    assert card.serialize() == {
        'id': id,
        'position': position.serialize(),
        'text': text,
        'type': type.value,
        'font': font.serialize(),
        'color': color,
        'dimension': dimension
    }


def test_board_object_card_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    color = 'light blue'
    dimension = [130, 130]
    serialized = {
        'id': id,
        'position': position.serialize(),
        'text': text,
        'type': type.value,
        'font': font.serialize(),
        'color': color,
        'dimension': dimension
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectCard.from_serialized(serialized, broker)
    assert card.id == id
    assert card.type == type
    assert card.position == position
    assert card.text == text
    assert card.font == font
    assert card.color == color
    assert card.dimension == dimension
