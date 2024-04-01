from .card import BoardObjectCard
from internal.models import Position
import uuid
import internal.pub_sub.mocks


def test_board_object_card_serialization():
    id = uuid.uuid4()
    position = Position(1, 2, 3)
    text = 'text'

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectCard(id, position, broker, text)
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

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    board = BoardObjectCard.from_serialized(serialized, broker)
    assert board.id == id
    assert board.position == position
    assert board.text == text
