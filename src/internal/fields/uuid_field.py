from __future__ import annotations
import uuid

from . import SerializableFieldBase


class UuidField(SerializableFieldBase):
    def __init__(self, val: uuid.UUID):
        super().__init__(val)

    def serialize(self) -> str:
        return str(self.value)

    @staticmethod
    def from_serialized(serialized: str) -> UuidField:
        return UuidField(uuid.UUID(serialized))
