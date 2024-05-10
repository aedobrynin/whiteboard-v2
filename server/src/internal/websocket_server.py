import logging
from typing import Mapping, Any

import y_py as Y
from pymongo.database import Database
from ypy_websocket import WebsocketServer, YRoom

_Y_DOC_OBJECTS_FIELD_NAME = 'objects'


class WebsocketServerWithDB(WebsocketServer):
    _db: Database[Mapping[str, Any]]

    def __init__(self, db: Database[Mapping[str, Any]]):
        WebsocketServer.__init__(self, auto_clean_rooms=False)
        self._db = db

    def transaction_callback_obj(self, event: Y.YMapEvent, room_name):
        logging.debug('callback function started')
        board_collection = self._db[room_name]
        logging.debug('successfully get collection (room_name) %s', board_collection.name)
        for obj_id, change in event.keys.items():
            new_data = change['newValue']
            if change['action'] == 'add':
                new_data['_id'] = obj_id
                board_collection.insert_one(new_data)
            elif change['action'] == 'update':
                if board_collection.find_one({'_id': obj_id}) is not None:
                    board_collection.update_one({'_id': obj_id}, {'$set': new_data})
                else:
                    new_data['_id'] = obj_id
                    board_collection.insert_one(new_data)

            elif change['action'] == 'delete':
                board_collection.delete_one({'_id': obj_id})
        logging.debug('callback function finished')

    async def start_room(self, room: YRoom):
        await super().start_room(room)
        room_name = super().get_room_name(room)[1:]
        logging.debug('room=%s started', room_name)
        board_collection = self._db[room_name]
        logging.debug('created collection')
        doc_ymap = room.ydoc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)
        doc_ymap.observe(lambda event: self.transaction_callback_obj(event, room_name))
        logging.debug('set up callback')
        obj_count = 0
        for key, value in doc_ymap.items():
            obj_count += 1
        logging.debug('ymap object counts=%s', obj_count)
        # updated_count = 0
        # for obj in board_collection.find():
        #     obj_id = obj['_id']
        #     for key, value in obj[]
        #     with room.ydoc.begin_transaction() as t:
        #         for params
        #         doc_ymap.set(t, , obj)
        #         updated_count += 1
        # logging.debug('updated objects=%d', updated_count)
