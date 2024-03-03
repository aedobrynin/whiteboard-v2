from . import ObjectBase, FieldUpdateInfo
from internal.fields.int_field import IntField


class ObjectExample(ObjectBase):
    counter: int

    def __init__(self, counter_value):
        super().__init__()
        super()._add_field('counter', IntField(counter_value))


def test_field_access():
    o = ObjectExample(0)
    assert o.counter == 0
    assert isinstance(o.counter, int)


def test_field_update():
    o = ObjectExample(1)
    assert o.get_changed_fields() == []

    o.counter = 8
    assert o.get_changed_fields() == [
        FieldUpdateInfo(field_name='counter', initial_value=1, current_value=8)
    ]

    o.counter = 1
    assert o.get_changed_fields() == []
