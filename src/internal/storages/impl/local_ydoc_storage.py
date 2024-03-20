from __future__ import annotations
from typing import Optional

import y_py

from .. import interfaces

_Y_DOC_OBJECTS_FIELD_NAME = 'objects'


class LocalYDocStorage(interfaces.IStorage):
    def __init__(self):
        self._y_doc = y_py.YDoc()
        self._objects = self._y_doc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)

    # Returns all objects from storage
    def get_serialized_objects(self) -> dict[interfaces.StorageKey, interfaces.StorageValue]:
        return dict(self._objects)

    # TODO: better api for updates
    def update(self, updates: dict[interfaces.StorageKey, Optional[interfaces.StorageValue]]):
        tx = self._y_doc.begin_transaction()
        for obj_id, new_repr in updates.items():
            if new_repr is None:
                self._objects.pop(tx, str(obj_id))
            else:
                # TODO: new repr should be YMap
                # Right now we trigger change event on the whole object, not on the particular properties
                self._objects.set(tx, str(obj_id), new_repr)
        del tx
