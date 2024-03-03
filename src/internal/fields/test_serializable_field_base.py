from . import SerializableFieldBase


def test_serializable_field_base_init():
    field = SerializableFieldBase(3)
    assert field.get_initial_value() == 3
    assert field.value == 3


def test_serializable_field_update():
    field = SerializableFieldBase(3)
    field.value = 5
    assert field.get_initial_value() == 3
    assert field.value == 5


def test_serializable_field_is_changed():
    field = SerializableFieldBase(3)
    assert not field.is_changed()

    field.value = 8
    assert field.is_changed()

    field.value = 3
    assert not field.is_changed()


def test_serializable_field_after_value_change():
    z = SerializableFieldBase(18)

    def after_value_change():
        z.value = 8

    field = SerializableFieldBase(3, after_value_change)
    assert z.value == 18
    field.value = 15
    assert z.value == 8
    assert z.get_initial_value() == 18
