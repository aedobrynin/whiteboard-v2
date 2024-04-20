import internal.objects
import internal.pub_sub.mocks

from .impl.card import BoardObjectCard
from .impl.object_id import generate_object_id


def test_card_building():
    serialized_card = {
        'type': 'card',
        'id': generate_object_id(),
        'position': {'x': 1, 'y': 2, 'z': 3},
        'text': 'text',
    }

    broker = internal.pub_sub.mocks.MockPubSubBroker()

    card = internal.objects.build_from_serialized(serialized_card, broker)
    assert isinstance(card, BoardObjectCard)
    assert card.serialize() == serialized_card
