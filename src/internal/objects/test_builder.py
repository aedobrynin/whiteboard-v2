import uuid

import internal.objects
from .impl.card import BoardObjectCard
import internal.pub_sub.mocks


def test_card_building():
    serialized_card = {
        'type': 'card',
        'id': str(uuid.uuid4()),
        'position': {'x': 1, 'y': 2, 'z': 3},
        'text': 'text',
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = internal.objects.build_from_serialized(serialized_card, broker)
    assert isinstance(card, BoardObjectCard)
    assert card.serialize() == serialized_card
