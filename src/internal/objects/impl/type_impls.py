import typing

from ..types import BoardObjectType
from .card import BoardObjectCard
from .text import BoardObjectText

TYPE_IMPLS: dict[BoardObjectType, typing.Type] = {
    BoardObjectType.CARD: BoardObjectCard,
    BoardObjectType.TEXT: BoardObjectText
}


assert len(TYPE_IMPLS) == len(BoardObjectType)
