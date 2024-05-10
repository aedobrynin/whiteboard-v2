import typing

from ..types import BoardObjectType
from .card import BoardObjectCard
from .text import BoardObjectText
from .pen import BoardObjectPen
from .group import BoardObjectGroup

TYPE_IMPLS: dict[BoardObjectType, typing.Type] = {
    BoardObjectType.CARD: BoardObjectCard,
    BoardObjectType.TEXT: BoardObjectText,
    BoardObjectType.PEN: BoardObjectPen,
    BoardObjectType.GROUP: BoardObjectGroup
}

assert len(TYPE_IMPLS) == len(BoardObjectType)
