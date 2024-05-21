from __future__ import annotations

import dataclasses

_X_FIELD = 'x'
_Y_FIELD = 'y'
_Z_FIELD = 'z'


@dataclasses.dataclass
class Position:
    x: int
    y: int
    z: int

    def __add__(self, other: Position):
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Position):
        return Position(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Position(-self.x, -self.y, -self.z)

    def serialize(self) -> dict:
        return {_X_FIELD: self.x, _Y_FIELD: self.y, _Z_FIELD: self.z}

    @staticmethod
    def from_serialized(data: dict) -> Position:
        return Position(data[_X_FIELD], data[_Y_FIELD], data[_Z_FIELD])
