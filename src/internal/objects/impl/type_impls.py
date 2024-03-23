import typing

from ..types import BoardObjectType
from .card import BoardObjectCard

TYPE_IMPLS: dict[BoardObjectType, typing.Type] = {
    BoardObjectType.card: BoardObjectCard,
}


assert len(TYPE_IMPLS) == len(BoardObjectType)
