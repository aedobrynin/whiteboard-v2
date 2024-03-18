from typing import Type

registered_types: dict[str, Type] = dict()


def board_object_type(name: str):
    def decorator(cls):
        registered_types[name] = cls
        return cls

    return decorator
