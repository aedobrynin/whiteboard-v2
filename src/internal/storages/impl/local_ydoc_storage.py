from __future__ import annotations
import pathlib
import logging
import sys

import y_py

from .ydoc_storage import YDocStorage, _Y_DOC_OBJECTS_FIELD_NAME
from .. import interfaces


class LocalYDocStorage(YDocStorage, interfaces.ILocalStorage):
    def __init__(self, store_path: pathlib.Path):
        YDocStorage.__init__(self)

        self._store_path = store_path
        self._load_from_file()

    def _load_from_file(self):
        if self._store_path.exists():
            logging.info('storage file exists')
            try:
                with open(self._store_path, 'rb') as f:
                    y_py.apply_update(self._y_doc, f.read())
            except OSError as e:
                # TODO: myb do not exit on the error
                logging.error(
                    'error on store file reading. store_path=%s, error=%s', self._store_path, e
                )
                sys.exit(1)
        else:
            logging.info("storage file doesn't exist")

        self._objects = self._y_doc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)

    def save(self):
        logging.info('saving objects to store_path=%s', self._store_path)
        with open(self._store_path, 'wb') as f:
            f.write(y_py.encode_state_as_update(self._y_doc))
