import internal.objects
import internal.pub_sub.mocks
from .impl.card import BoardObjectCard
from .impl.connector import BoardObjectConnector
from .impl.object_id import generate_object_id
from .impl.text import BoardObjectText


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


def test_connector_building():
    serialized_connector = {
        'id': generate_object_id(),
        'type': 'connector',
        'start_id': generate_object_id(),
        'end_id': generate_object_id(),
        'color': 'black',
        'width': 2.0,
        'connector_type': 'curved',
        'stroke_style': 'left'
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    connector = internal.objects.build_from_serialized(serialized_connector, broker)
    assert isinstance(connector, BoardObjectConnector)
    assert connector.serialize() == serialized_connector
