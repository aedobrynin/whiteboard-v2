from __future__ import annotations
from typing import Optional

import internal.repositories.interfaces
import internal.objects.interfaces
import internal.repositories.exceptions


class Repository(internal.repositories.interfaces.IRepository):
    def __init__(self, objects: list[internal.objects.interfaces.IBoardObject]):
        self._objects: dict[
            internal.objects.interfaces.ObjectId, internal.objects.interfaces.IBoardObject
        ] = dict()
        self._cached_serialized_representations: dict[
            internal.objects.interfaces.ObjectId, Optional[dict]
        ] = dict()
        self._deleted_object_ids: list[internal.objects.interfaces.ObjectId] = []

        for object in objects:
            self._objects[object.id] = object
            self._cached_serialized_representations[object.id] = object.serialize()

    def get(
        self, object_id: internal.objects.interfaces.ObjectId
    ) -> Optional[internal.objects.interfaces.IBoardObject]:
        return self._objects.get(object_id, None)

    def add(self, object: internal.objects.interfaces.IBoardObject) -> None:
        if object.id in self._objects:
            raise internal.repositories.exceptions.ObjectAlreadyExistsException()
        self._objects[object.id] = object

    def delete(self, object_id: internal.objects.interfaces.ObjectId) -> None:
        if object_id not in self._objects:
            raise internal.repositories.exceptions.ObjectNotFound()
        del self._objects[object_id]
        self._cached_serialized_representations[object_id] = None

        self._deleted_object_ids.append(object_id)

    # TODO: optimize this
    def get_updated(self) -> dict[internal.objects.interfaces.ObjectId, Optional[dict]]:
        updated_representations: dict[internal.objects.interfaces.ObjectId, Optional[dict]] = dict()
        for object in self._objects.values():
            serialized = object.serialize()
            if serialized != self._cached_serialized_representations.get(object.id, None):
                updated_representations[object.id] = serialized
                self._cached_serialized_representations[object.id] = serialized

        for obj_id in self._deleted_object_ids:
            updated_representations[obj_id] = None
        self._deleted_object_ids = []

        return updated_representations
