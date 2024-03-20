from __future__ import annotations
import abc
from typing import Optional

StorageKey = str
StorageValue = dict


class IStorage(abc.ABC):
    # TODO: ability to save from file and load from file

    # Returns all objects from storage
    @abc.abstractmethod
    def get_serialized_objects(self) -> dict[StorageKey, StorageValue]:
        pass

    # TODO: better api for updates
    @abc.abstractmethod
    def update(self, updates: dict[StorageKey, Optional[StorageValue]]):
        pass


# TODO: implement when needed
# Should have method `get_updates()`
# which will be applied to objects
class ISharedStorage(IStorage):
    pass
