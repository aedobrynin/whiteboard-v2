from .impl.type_impls import TYPE_IMPLS
from .impl.common import field_names
from . import interfaces
from .types import BoardObjectType


def build_from_serialized(data: dict) -> interfaces.IBoardObject:
    return TYPE_IMPLS[BoardObjectType(data[field_names.TYPE_FIELD])].from_serialized(data)
