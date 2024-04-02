from __future__ import annotations

import y_py

from .. import interfaces

_Y_DOC_OBJECTS_FIELD_NAME = 'objects'


class YDocStorage(interfaces.IStorage):
    def __init__(self):
        self._y_doc = y_py.YDoc()
        self._objects = self._y_doc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)

    def get_serialized_objects(
        self,
    ) -> dict[interfaces.IStorage.StorageKey, interfaces.IStorage.StorageValue]:
        return dict(self._objects)

    # TODO: better api for updates
    def update(self, updates: interfaces.IStorage.UpdatesType):
        with self._y_doc.begin_transaction() as tx:
            for obj_id, new_repr in updates.items():
                if new_repr is None:
                    self._objects.pop(tx, str(obj_id))
                else:
                    # TODO: new repr should be YMap
                    # Right now we trigger change event on the whole object,
                    # not on the particular properties
                    self._objects.set(tx, str(obj_id), new_repr)
