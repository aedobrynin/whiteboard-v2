from __future__ import annotations

from typing import List

from internal.objects import interfaces
import internal.models
import internal.pub_sub.interfaces
from .object_with_position import BoardObjectWithPosition
from .common import field_names
from .. import types

_TEXT_FIELD = 'text'
_FONT_SLANT_FIELD = 'font-slant'
_FONT_WEIGHT_FIELD = 'font-weight'
_FONT_COLOR_FIELD = 'font-color'
_FONT_FAMILY_FIELD = 'font-family'
_FONT_SIZE_FIELD = 'font-size'


class BoardObjectText(interfaces.IBoardObjectText, BoardObjectWithPosition):
    def __init__(
        self,
        id: interfaces.ObjectId,
        position: internal.models.Position,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        text: str = 'text',
        font_slant: str = 'roman',  # TODO: make enums, maybe font class
        font_weight: str = 'normal',
        font_color: str = 'black',
        font_family: str = 'Arial',
        font_size: float = 14
    ):
        super().__init__(id, types.BoardObjectType.TEXT, position, pub_sub_broker)
        self.text = text
        self.font_slant = font_slant
        self.font_weight = font_weight
        self.font_color = font_color
        self.font_family = font_family
        self.font_size = font_size

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    @property
    def font_slant(self) -> str:
        return self._font_slant

    @font_slant.setter
    def font_slant(self, font_slant: str) -> None:
        self._font_slant = font_slant

    @property
    def font_weight(self) -> str:
        return self._font_weight

    @font_weight.setter
    def font_weight(self, font_weight: str) -> None:
        self._font_weight = font_weight

    @property
    def font_color(self) -> str:
        return self._font_color

    @font_color.setter
    def font_color(self, font_color: str) -> None:
        self._font_color = font_color

    @property
    def font_family(self) -> str:
        return self._font_family

    @font_family.setter
    def font_family(self, font_family: str) -> None:
        self._font_family = font_family

    @property
    def font_size(self) -> float:
        return self._font_size

    @font_size.setter
    def font_size(self, font_size: float) -> None:
        self._font_size = font_size

    @property
    def props(self) -> List[str]:
        return [
            _TEXT_FIELD,
            _FONT_SLANT_FIELD,
            _FONT_WEIGHT_FIELD,
            _FONT_COLOR_FIELD,
            _FONT_FAMILY_FIELD,
            _FONT_SIZE_FIELD
        ]

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized[_TEXT_FIELD] = self.text
        serialized[_FONT_SLANT_FIELD] = self.font_slant
        serialized[_FONT_WEIGHT_FIELD] = self.font_weight
        serialized[_FONT_COLOR_FIELD] = self.font_color
        serialized[_FONT_FAMILY_FIELD] = self.font_family
        serialized[_FONT_SIZE_FIELD] = self.font_size
        return serialized

    @staticmethod
    def from_serialized(
        data: dict,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ) -> BoardObjectText:
        # TODO: child class should not know how to build parent from serialized data
        return BoardObjectText(
            interfaces.ObjectId(data[field_names.ID_FIELD]),
            internal.models.Position.from_serialized(data[field_names.POSITION_FIELD]),
            pub_sub_broker,
            data[_TEXT_FIELD],
            data[_FONT_SLANT_FIELD],
            data[_FONT_WEIGHT_FIELD],
            data[_FONT_COLOR_FIELD],
            data[_FONT_FAMILY_FIELD],
            data[_FONT_SIZE_FIELD],
        )
