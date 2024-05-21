import typing

from .card import BoardObjectCard
from .connector import BoardObjectConnector
from .group import BoardObjectGroup
from .pen import BoardObjectPen
from .text import BoardObjectText
from ..types import BoardObjectType

TYPE_IMPLS: dict[BoardObjectType, typing.Type] = {
    BoardObjectType.CARD: BoardObjectCard,
    BoardObjectType.TEXT: BoardObjectText,
    BoardObjectType.PEN: BoardObjectPen,
    BoardObjectType.GROUP: BoardObjectGroup,
    BoardObjectType.CONNECTOR: BoardObjectConnector
}

assert len(TYPE_IMPLS) == len(BoardObjectType)
