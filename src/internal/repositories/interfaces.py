from __future__ import annotations
import abc
import uuid
from typing import Optional

import internal.objects


class IRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, object_id: uuid.UUID) -> Optional[internal.objects.interfaces.IBoardObject]:
        pass

    # raises ObjectAlreadyExistsException if object with the same id already in the repository
    @abc.abstractmethod
    def add(self, object: internal.objects.interfaces.IBoardObject) -> None:
        pass

    # raises ObjectNotFoundException if object with such id was not found
    # TODO: myb somehow invalidate objects that were deleted (e.g. raise on read/write access to their fields)
    @abc.abstractmethod
    def delete(self, object_id: uuid.UUID) -> None:
        pass

    # Returns serialized objects which were updated, created or deleted since last `get_updated()` call
    # If object was deleted, this function returns None for it's representation
    # TODO: myb return only updated fields
    # TODO: myb better API for deleted objects
    @abc.abstractmethod
    def get_updated(self) -> dict[uuid.UUID, Optional[dict]]:
        pass


# TODO: implement when needed
class IObjectsWithPositionRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: IRepository):
        pass

    @abc.abstractmethod
    def get(
        self, object_id: uuid.UUID
    ) -> Optional[internal.objects.interfaces.IBoardObjectWithPosition]:
        pass


# TODO: implement when needed
class ICardRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo: IRepository):
        pass

    @abc.abstractmethod
    def get(self, object_id: uuid.UUID) -> Optional[internal.objects.interfaces.IBoardObjectCard]:
        pass
