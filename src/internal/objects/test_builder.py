import uuid

import internal.objects
from .impl.card import BoardObjectCard


def test_card_building():
    serialized_card = {
        'type': 'card',
        'id': str(uuid.uuid4()),
        'position': {'x': 1, 'y': 2, 'z': 3},
        'text': 'text',
    }

    card = internal.objects.build_from_serialized(serialized_card)
    assert isinstance(card, BoardObjectCard)
    assert card.serialize() == serialized_card
