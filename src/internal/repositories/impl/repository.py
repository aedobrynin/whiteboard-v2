from __future__ import annotations
from typing import Optional
import logging

import internal.objects.interfaces
from .. import interfaces
from .. import exceptions


class Repository(interfaces.IRepository):
    # TODO: allow repo to be built from serialized objects
    def __init__(self, objects: list[internal.objects.interfaces.IBoardObject]):
        logging.debug('initializing repository with %d objects', len(objects))

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
        obj = self._objects.get(object_id, None)
        logging.debug('getting object with id=%s, is_present=%d', str(object_id), obj is not None)
        return obj

    def add(self, object: internal.objects.interfaces.IBoardObject) -> None:
        logging.debug('trying to add object with id=%s', str(object.id))
        if object.id in self._objects:
            raise exceptions.ObjectAlreadyExistsException()
        self._objects[object.id] = object

    def delete(self, object_id: internal.objects.interfaces.ObjectId) -> None:
        logging.debug('trying to delete object with id=', str(object_id))
        if object_id not in self._objects:
            raise exceptions.ObjectNotFound()
        del self._objects[object_id]
        self._cached_serialized_representations[object_id] = None

        self._deleted_object_ids.append(object_id)

    # TODO: optimize this
    def get_updated(self) -> dict[internal.objects.interfaces.ObjectId, Optional[dict]]:
        logging.debug('building updated objects')
        updated_representations: dict[internal.objects.interfaces.ObjectId, Optional[dict]] = dict()
        for object in self._objects.values():
            serialized = object.serialize()
            if serialized != self._cached_serialized_representations.get(object.id, None):
                updated_representations[object.id] = serialized
                self._cached_serialized_representations[object.id] = serialized

        for obj_id in self._deleted_object_ids:
            updated_representations[obj_id] = None
        self._deleted_object_ids = []

        logging.debug('there are %d updated objects', len(updated_representations))
        return updated_representations
