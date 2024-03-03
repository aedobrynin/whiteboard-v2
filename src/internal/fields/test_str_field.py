from . import StrField


def test_int_field_init():
    field = StrField('data')
    assert field.get_initial_value() == 'data'
    assert field.value == 'data'


def test_int_field_serialize():
    field = StrField('data')
    field.value = 'updated_data'
    assert field.serialize() == 'updated_data'


def test_int_field_from_serialized():
    field = StrField.from_serialized('data')
    assert field.value == 'data'
