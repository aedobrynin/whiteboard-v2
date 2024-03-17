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

    def serialize(self) -> dict:
        return {_X_FIELD: self.x, _Y_FIELD: self.y, _Z_FIELD: self.z}

    @staticmethod
    def from_serialized(data: dict) -> Position:
        return Position(data[_X_FIELD], data[_Y_FIELD], data[_Z_FIELD])
