from __future__ import annotations

from . import SerializableFieldBase


class IntField(SerializableFieldBase):
    def __init__(self, val: int):
        super().__init__(val)

    def serialize(self) -> int:
        return self.value

    @staticmethod
    def from_serialized(serialized: int) -> IntField:
        return IntField(serialized)
