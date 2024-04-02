from __future__ import annotations
import abc
from typing import Optional

import internal.objects

REPOSITORY_PUB_SUB_ID = 'repository'


class IRepository(abc.ABC):
    @abc.abstractmethod
    def get(
        self, object_id: internal.objects.interfaces.ObjectId
    ) -> Optional[internal.objects.interfaces.IBoardObject]:
        pass

    # raises ObjectAlreadyExistsException if object with the same id already in the repository
    # TODO: published event description
    @abc.abstractmethod
    def add(self, object: internal.objects.interfaces.IBoardObject) -> None:
        pass

    # raises ObjectNotFoundException if object with such id was not found
    # TODO: myb somehow invalidate objects that were deleted (e.g. raise on read/write access to their fields)
    # TODO: published event description
    @abc.abstractmethod
    def delete(self, object_id: internal.objects.interfaces.ObjectId) -> None:
        pass

    # Returns serialized objects which were updated, created or deleted since last `get_updated()` call
    # If object was deleted, this function returns None for it's representation
    # TODO: myb return only updated fields
    # TODO: myb better API for deleted objects
    # TODO: move it to another interface (because now it is accessible from any object)
    @abc.abstractmethod
    def get_updated(self) -> dict[internal.objects.interfaces.ObjectId, Optional[dict]]:
        pass


# TODO: implement when needed
class IObjectsWithPositionRepository(IRepository):
    @abc.abstractmethod
    def __init__(self, repo: IRepository):
        pass

    @abc.abstractmethod
    def get(
        self, object_id: internal.objects.interfaces.ObjectId
    ) -> Optional[internal.objects.interfaces.IBoardObjectWithPosition]:
        pass


# TODO: implement when needed
class ICardRepository(IObjectsWithPositionRepository):
    @abc.abstractmethod
    def __init__(self, repo: IRepository):
        pass

    @abc.abstractmethod
    def get(
        self, object_id: internal.objects.interfaces.ObjectId
    ) -> Optional[internal.objects.interfaces.IBoardObjectCard]:
        pass
