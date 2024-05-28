from datetime import datetime

import internal.objects
import internal.pub_sub.mocks
from .impl.card import BoardObjectCard
from .impl.group import BoardObjectGroup
from .impl.text import BoardObjectText
from .impl.connector import BoardObjectConnector
from .impl.table import BoardObjectTable
from .impl.object_id import generate_object_id


def test_text_building():
    serialized_text = {
        'type': 'text',
        'id': generate_object_id(),
        'create_dttm': datetime.now().replace(microsecond=0).strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': {'x': 1, 'y': 2, 'z': 3},
        'text': 'text',
        'font': {
            'slant': 'roman',
            'weight': 'normal',
            'color': 'black',
            'family': 'Arial',
            'size': 14,
        },
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    text = internal.objects.build_from_serialized(serialized_text, broker)
    assert isinstance(text, BoardObjectText)
    assert text.serialize() == serialized_text


def test_card_building():
    serialized_card = {
        'type': 'card',
        'id': generate_object_id(),
        'create_dttm': datetime.now().replace(microsecond=0).strftime('%Y-%m-%dT%H-%M-%SZ'),
        'position': {'x': 1, 'y': 2, 'z': 3},
        'text': 'text',
        'font': {
            'slant': 'roman',
            'weight': 'normal',
            'color': 'black',
            'family': 'Arial',
            'size': 14,
        },
        'color': 'light yellow',
        'width': 100,
        'height': 150,
        'attribute': {'age': '10'}
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = internal.objects.build_from_serialized(serialized_card, broker)
    assert isinstance(card, BoardObjectCard)
    assert card.serialize() == serialized_card


def test_group_building():
    serialized_card = {
        'type': 'group',
        'create_dttm': datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ'),
        'id': generate_object_id(),
        'children_ids': [generate_object_id, generate_object_id],
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    group = internal.objects.build_from_serialized(serialized_card, broker)
    assert isinstance(group, BoardObjectGroup)
    assert group.serialize() == serialized_card


def test_connector_building():
    serialized_connector = {
        'id': generate_object_id(),
        'type': 'connector',
        'create_dttm': datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ'),
        'start_id': generate_object_id(),
        'end_id': generate_object_id(),
        'color': 'black',
        'width': 2,
        'connector_type': 'curved',
        'stroke_style': 'left',
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    connector = internal.objects.build_from_serialized(serialized_connector, broker)
    assert isinstance(connector, BoardObjectConnector)
    assert connector.serialize() == serialized_connector


def test_table_building():
    serialized_table = {
        'id': generate_object_id(),
        'create_dttm': datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ'),
        'type': 'table',
        'position': {'x': 1, 'y': 2, 'z': 3},
        'table-columns': 2,
        'table-rows': 2,
        'columns-width': [50, 50],
        'rows-height': [50, 50],
        'default-width': 50,
        'default-height': 50,
        'linked-objects': {},
    }
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    table = internal.objects.build_from_serialized(serialized_table, broker)
    assert isinstance(table, BoardObjectTable)
    assert table.serialize() == serialized_table
