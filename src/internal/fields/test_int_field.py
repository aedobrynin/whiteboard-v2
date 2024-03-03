from . import IntField


def test_int_field_init():
    field = IntField(3)
    assert field.get_initial_value() == 3
    assert field.value == 3


def test_int_field_serialize():
    field = IntField(3)
    field.value = 5
    assert field.serialize() == 5


def test_int_field_from_serialized():
    field = IntField.from_serialized(5)
    assert field.value == 5
