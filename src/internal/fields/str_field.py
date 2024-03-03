from __future__ import annotations

from . import SerializableFieldBase


class StrField(SerializableFieldBase):
    def __init__(self, val: str):
        super().__init__(val)

    def serialize(self) -> str:
        return self.value

    @staticmethod
    def from_serialized(serialized: str) -> StrField:
        return StrField(serialized)
