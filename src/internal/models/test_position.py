from . import Position


def test_position_serialization():
    p = Position(1, 2, 3)
    assert p.serialize() == {'x': 1, 'y': 2, 'z': 3}
    p_copy = Position.from_serialized(p.serialize())
    assert p == p_copy
