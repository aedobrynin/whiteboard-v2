from .impl.registered_types import registered_types
from .impl.common import field_names
from . import interfaces


def build_from_serialized(data: dict) -> interfaces.IBoardObject:
    return registered_types[data[field_names.TYPE_FIELD]].from_serialized(data)
