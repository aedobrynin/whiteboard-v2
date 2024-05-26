from __future__ import annotations

import os
import queue
from typing import Optional

from y_py import YMapEvent
from ypy_websocket import WebsocketProvider
from ypy_websocket.websocket import Websocket

from .ydoc_storage import YDocStorage, _Y_DOC_OBJECTS_FIELD_NAME
from .. import interfaces

# TODO: .env file
SERVER_HOST = os.environ.get('SERVER_HOST', '51.250.90.146')
SERVER_PORT = os.environ.get('SERVER_PORT', 5000)
URI_WEBSOCKET_SERVER = f'ws://{SERVER_HOST}:{SERVER_PORT}'


class SharedYDocStorage(YDocStorage, interfaces.ISharedStorage):

    def __init__(self, board_name: str, board_key: str):
        YDocStorage.__init__(self)
        self._board_name = board_name
        self._board_key = board_key
        self._cur_changes = queue.Queue()
        doc_ymap = self._y_doc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)
        doc_ymap.observe(self._transaction_callback_obj)

    def get_uri_connection(self):
        return f'{URI_WEBSOCKET_SERVER}/{self._board_key}'

    def get_websocket_provider(self, websocket: Websocket):
        return WebsocketProvider(self._y_doc, websocket)

    def _transaction_callback_obj(self, event: YMapEvent):
        for obj_id, change in event.keys.items():
            obj = dict()
            obj['obj_repr'] = change['newValue'] if change['action'] != 'delete' else None
            obj['obj_action'] = change['action']
            obj['obj_id'] = obj_id
            self._cur_changes.put(obj)

    def is_empty_updates(self):
        return self._cur_changes.empty()

    def get_updates(self) -> Optional[dict]:
        while not self._cur_changes.empty():
            yield self._cur_changes.get()
