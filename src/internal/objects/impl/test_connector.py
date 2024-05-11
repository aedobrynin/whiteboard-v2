import internal.pub_sub.mocks
from .connector import BoardObjectConnector
from .object_id import generate_object_id
from ..types import BoardObjectType


def test_board_connector_serialization():
    id = generate_object_id()
    type = BoardObjectType.CONNECTOR
    start_id = generate_object_id()
    end_id = generate_object_id()
    color = 'black'
    width = 2.0
    connector_type = 'curved'
    stroke_style = 'left'
    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj = BoardObjectConnector(
        id, broker, start_id, end_id, color, width, connector_type, stroke_style
    )
    assert obj.serialize() == {
        'id': id,
        'type': type.value,
        'start_id': start_id,
        'end_id': end_id,
        'color': color,
        'width': width,
        'connector_type': connector_type,
        'stroke_style': stroke_style
    }


def test_board_connector_deserialization():
    id = generate_object_id()
    type = BoardObjectType.CONNECTOR
    start_id = generate_object_id()
    end_id = generate_object_id()
    color = 'black'
    width = 2.0
    connector_type = 'curved'
    stroke_style = 'left'

    serialized = {
        'id': id,
        'type': type.value,
        'start_id': start_id,
        'end_id': end_id,
        'color': color,
        'width': width,
        'connector_type': connector_type,
        'stroke_style': stroke_style
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    obj: BoardObjectConnector = BoardObjectConnector.from_serialized(serialized, broker)
    assert obj.id == id
    assert obj.type == type
    assert obj.start_id == start_id
    assert obj.end_id == end_id
    assert obj.color == color
    assert obj.width == width
    assert obj.connector_type == connector_type
    assert obj.stroke_style == stroke_style
