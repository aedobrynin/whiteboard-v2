from typing import Type

from ..interfaces import IBoardObject

registered_types: dict[str, Type[IBoardObject]] = dict()


def board_object_type(name: str):
    def decorator(cls):
        registered_types[name] = cls
        return cls

    return decorator
