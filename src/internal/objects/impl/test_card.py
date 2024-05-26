from datetime import datetime

import internal.pub_sub.mocks
from internal.models import Position, Font
from .card import BoardObjectCard
from .object_id import generate_object_id
from ..types import BoardObjectType


def test_board_object_card_serialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    color = 'light blue'
    width = 100
    height = 150
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectCard(id, create_dttm, position, broker, text, font, color, width, height)
    assert card.serialize() == {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': position.serialize(),
        'text': text,
        'type': type.value,
        'font': font.serialize(),
        'color': color,
        'width': width,
        'height': height,
    }


def test_board_object_card_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CARD
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    text = 'text'
    font = Font()
    color = 'light blue'
    width = 100
    height = 150
    serialized = {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': position.serialize(),
        'text': text,
        'type': type.value,
        'font': font.serialize(),
        'color': color,
        'width': width,
        'height': height,
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectCard.from_serialized(serialized, broker)
    assert card.id == id
    assert card.create_dttm == create_dttm
    assert card.type == type
    assert card.position == position
    assert card.text == text
    assert card.font == font
    assert card.color == color
    assert card.width == width
    assert card.height == height
