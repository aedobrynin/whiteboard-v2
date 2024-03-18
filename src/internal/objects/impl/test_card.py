from . import BoardObjectCard
from internal.models import Position
from .registered_types import registered_types
import uuid


def test_board_object_card_in_registered_types():
    assert registered_types['card'] == BoardObjectCard


def test_board_object_card_serialization():
    id = uuid.uuid4()
    position = Position(1, 2, 3)
    text = 'text'

    card = BoardObjectCard(id, position, text)
    assert card.serialize() == {
        'id': str(id),
        'position': position.serialize(),
        'text': text,
        'type': 'card',
    }


def test_board_object_card_deserialization():
    id = uuid.uuid4()
    position = Position(1, 2, 3)
    text = 'text'

    serialized = {
        'id': str(id),
        'position': position.serialize(),
        'text': text,
        'type': 'card',
    }

    board = BoardObjectCard.from_serialized(serialized)
    assert board.id == id
    assert board.position == position
    assert board.text == text
