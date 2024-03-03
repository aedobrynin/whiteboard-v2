from . import ObjectBase, FieldUpdateInfo
from internal.fields import IntField, StrField


class ObjectWithOneField(ObjectBase):
    counter: int

    def __init__(self, counter_value):
        super().__init__()
        super()._add_field('counter', IntField(counter_value))


def test_field_access():
    o = ObjectWithOneField(0)
    assert o.counter == 0
    assert isinstance(o.counter, int)


def test_field_update():
    o = ObjectWithOneField(1)
    assert o.get_changed_fields() == []

    o.counter = 8
    assert o.get_changed_fields() == [
        FieldUpdateInfo(field_name='counter', initial_value=1, current_value=8)
    ]

    o.counter = 1
    assert o.get_changed_fields() == []


class ObjectWithManyFields(ObjectBase):
    counter: int
    label: str

    def __init__(self, counter_value, label_value):
        super().__init__()
        super()._add_field('counter', IntField(counter_value))
        super()._add_field('label', StrField(label_value))


def test_many_fields_update():
    o = ObjectWithManyFields(5, 'counter')
    o.counter = 15
    o.label = 'LABEL'

    assert o.get_changed_fields() == [
        FieldUpdateInfo(field_name='counter', initial_value=5, current_value=15),
        FieldUpdateInfo(field_name='label', initial_value='counter', current_value='LABEL'),
    ]
