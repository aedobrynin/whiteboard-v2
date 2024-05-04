import typing

from ..types import BoardObjectType
from .card import BoardObjectCard
from .text import BoardObjectText
from .pen import BoardObjectPen
from .table import BoardObjectTable

TYPE_IMPLS: dict[BoardObjectType, typing.Type] = {
    BoardObjectType.CARD: BoardObjectCard,
    BoardObjectType.TEXT: BoardObjectText,
    BoardObjectType.PEN: BoardObjectPen,
    BoardObjectType.TABLE: BoardObjectTable
}


assert len(TYPE_IMPLS) == len(BoardObjectType)
