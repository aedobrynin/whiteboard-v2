from __future__ import annotations
import pathlib
import abc
import uuid
from typing import Optional


class IStorage(abc.ABC):
    StorageKey = str
    StorageValue = dict
    UpdatesType = dict[StorageKey, Optional[StorageValue]]

    # Returns all objects from storage
    @abc.abstractmethod
    def get_serialized_objects(self) -> dict[StorageKey, StorageValue]:
        pass

    # TODO: better api for updates
    @abc.abstractmethod
    def update(self, updates: UpdatesType):
        pass


class ILocalStorage(IStorage):
    @abc.abstractmethod
    def __init__(self, store_path: pathlib.Path):
        pass

    @abc.abstractmethod
    def save(self):
        pass


# TODO: implement when needed
# Should have method `get_updates()`
# which will be applied to objects
class ISharedStorage(IStorage):
    BoardKey = uuid.uuid4

    @abc.abstractmethod
    def __init__(self, board_key: BoardKey):
        pass

    @abc.abstractmethod
    def is_empty_updates(self):
        pass

    @abc.abstractmethod
    def get_updates(self):
        pass
