from . import BoardObjectCard, Position

import uuid


def test_board_object_card_serialization():
    id = uuid.uuid4()
    position = Position(1, 2, 3)
    text = 'text'

    card = BoardObjectCard(id, position, text)
    assert card.serialize() == {
        'id': str(id),
        'position': {
            'x': position.x,
            'y': position.y,
            'z': position.z,
        },
        'text': text,
    }


def test_board_object_card_deserialization():
    id = uuid.uuid4()
    position = Position(1, 2, 3)
    text = 'text'

    serialized = {
        'id': str(id),
        'position': {
            'x': position.x,
            'y': position.y,
            'z': position.z,
        },
        'text': text,
    }

    board = BoardObjectCard.from_serialized(serialized)
    assert board.id == id
    assert board.position == position
    assert board.text == text
