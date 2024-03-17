from . import UuidField

import uuid


def test_uuid_field_init():
    val = uuid.uuid4()

    field = UuidField(val)
    assert field.get_initial_value() == val
    assert field.value == val


def test_uuid_field_serialize():
    val = uuid.uuid4()

    field = UuidField(val)
    assert field.serialize() == str(val)


def test_uuid_field_from_serialized():
    val = uuid.uuid4()

    field = UuidField.from_serialized(str(val))
    assert field.value == val
