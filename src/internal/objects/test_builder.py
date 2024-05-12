import internal.objects
import internal.pub_sub.mocks

from .impl.card import BoardObjectCard
from .impl.group import BoardObjectGroup
from .impl.text import BoardObjectText
from .impl.object_id import generate_object_id


def test_text_building():
    serialized_text = {
        'type': 'text',
        'id': generate_object_id(),
        'position': {'x': 1, 'y': 2, 'z': 3},
        'text': 'text',
        'font': {
            'slant': 'roman',
            'weight': 'normal',
            'color': 'black',
            'family': 'Arial',
            'size': 14
        }
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    text = internal.objects.build_from_serialized(serialized_text, broker)
    assert isinstance(text, BoardObjectText)
    assert text.serialize() == serialized_text


def test_card_building():
    serialized_card = {
        'type': 'card',
        'id': generate_object_id(),
        'position': {'x': 1, 'y': 2, 'z': 3},
        'text': 'text',
        'font': {
            'slant': 'roman',
            'weight': 'normal',
            'color': 'black',
            'family': 'Arial',
            'size': 14
        },
        'color': 'light yellow'
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = internal.objects.build_from_serialized(serialized_card, broker)
    assert isinstance(card, BoardObjectCard)
    assert card.serialize() == serialized_card


def test_group_building():
    serialized_card = {
        'type': 'group',
        'id': generate_object_id(),
        'children_ids': [generate_object_id, generate_object_id]
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    group = internal.objects.build_from_serialized(serialized_card, broker)
    assert isinstance(group, BoardObjectGroup)
    assert group.serialize() == serialized_card
