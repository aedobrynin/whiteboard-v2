from __future__ import annotations

_SLANT_FIELD = 'slant'
_WEIGHT_FIELD = 'weight'
_COLOR_FIELD = 'color'
_FAMILY_FIELD = 'family'
_SIZE_FIELD = 'size'


class Font:
    def __init__(
        self,
        slant: str = 'roman',
        weight: str = 'normal',
        color: str = 'black',
        family: str = 'Arial',
        size: float = 14,
    ):
        self.slant = slant
        self.weight = weight
        self.color = color
        self.family = family
        self.size = size

    # TODO: Add restrictions
    def update_fields(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def slant(self) -> str:
        return self._slant

    @slant.setter
    def slant(self, slant: str) -> None:
        self._slant = slant

    @property
    def weight(self) -> str:
        return self._weight

    @weight.setter
    def weight(self, weight: str) -> None:
        self._weight = weight

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        self._color = color

    @property
    def family(self) -> str:
        return self._family

    @family.setter
    def family(self, family: str) -> None:
        self._family = family

    @property
    def size(self) -> float:
        return self._size

    @size.setter
    def size(self, size: float) -> None:
        self._size = size

    def serialize(self) -> dict:
        return {
            _SLANT_FIELD: self.slant,
            _WEIGHT_FIELD: self.weight,
            _COLOR_FIELD: self.color,
            _FAMILY_FIELD: self.family,
            _SIZE_FIELD: self.size,
        }

    @staticmethod
    def from_serialized(data: dict) -> Font:
        return Font(
            data[_SLANT_FIELD],
            data[_WEIGHT_FIELD],
            data[_COLOR_FIELD],
            data[_FAMILY_FIELD],
            data[_SIZE_FIELD],
        )

    def __eq__(self, other):
        if not isinstance(other, Font):
            return False
        if self.slant != other.slant:
            return False
        if self.weight != other.weight:
            return False
        if self.color != other.color:
            return False
        if self.family != other.family:
            return False
        if self.size != other.size:
            return False
        return True

    def __repr__(self):
        return f"""Font(slant='{self.slant}', weight='{self.weight}', color='{self.color}', family='{self.family}', size='{self.size}')"""

    def __str__(self):
        return f"""Font(slant='{self.slant}', weight='{self.weight}', color='{self.color}', family='{self.family}', size='{self.size}')"""
