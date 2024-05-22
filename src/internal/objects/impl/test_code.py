from datetime import datetime

import internal.pub_sub.mocks
from internal.models import Position, Font
from .code import BoardObjectCode
from .object_id import generate_object_id
from ..types import BoardObjectType


def test_board_object_code_serialization():
    id = generate_object_id()
    type = BoardObjectType.CODE
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    text = 'print(2 + 2)'
    font = Font()
    lexer = 'python'
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = BoardObjectCode(id, create_dttm, position, broker, text, font, lexer)
    assert card.serialize() == {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': position.serialize(),
        'text': text,
        'type': type.value,
        'font': font.serialize(),
        'lexer': lexer,
    }


def test_board_object_code_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CODE
    create_dttm = datetime.now().replace(microsecond=0)
    position = Position(1, 2, 3)
    text = 'print(2 + 2)'
    font = Font()
    lexer = 'python'
    serialized = {
        'id': id,
        'create_dttm': create_dttm.strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': position.serialize(),
        'text': text,
        'type': type.value,
        'font': font.serialize(),
        'lexer': lexer,
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    code = BoardObjectCode.from_serialized(serialized, broker)
    assert code.id == id
    assert code.create_dttm == create_dttm
    assert code.type == type
    assert code.position == position
    assert code.text == text
    assert code.font == font
    assert code.lexer == lexer
