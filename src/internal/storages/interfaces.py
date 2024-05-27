import pathlib
import abc
import uuid
from typing import Optional
import asyncio

import internal.controller.interfaces
import internal.repository.interfaces


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


class ISharedStorage(IStorage):
    BoardKey = uuid.uuid4

    @abc.abstractmethod
    def __init__(self, board_key: BoardKey):
        pass

    @abc.abstractmethod
    def is_empty_updates(self):
        pass

    @abc.abstractmethod
    async def run(
        self,
        controller: internal.controller.interfaces.IController,
        repo: internal.repositories.interfaces.IRepository,
        stop: asyncio.Event,
    ):
        pass
