from __future__ import annotations

import logging

from pymongo.database import Database, Mapping, Any
from ypy_websocket import WebsocketServer, YRoom

_Y_DOC_OBJECTS_FIELD_NAME = 'objects'


class WebsocketServerWithDB(WebsocketServer):
    _db: Database[Mapping[str, Any]]

    def __init__(self, db: Database[Mapping[str, Any]]):
        WebsocketServer.__init__(self)
        self._db = db
        super()

    def update_ymap_from_database(self, room: YRoom):
        logging.debug('loading collection')
        room_name = self.get_room_name(room)[1:]
        board_collection = self._db[room_name]
        logging.debug('successfully loaded collection')
        doc_ymap = room.ydoc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)
        updated_count = 0
        for obj in board_collection.find():
            obj_repr = dict(obj)
            obj_id = obj_repr.pop('_id')
            with room.ydoc.begin_transaction() as t:
                doc_ymap.set(t, obj_id, obj_repr)
                updated_count += 1
        logging.debug('updated objects=%d', updated_count)

    def update_database_from_ymap(self, room: YRoom):
        logging.debug('loading collection')
        room_name = self.get_room_name(room)[1:]
        board_collection = self._db[room_name]
        logging.debug('successfully loaded collection')
        serialized_objects = dict(room.ydoc.get_map(_Y_DOC_OBJECTS_FIELD_NAME))
        # get unique keys
        obj_ids_collection = []
        for obj in board_collection.find():
            obj_ids_collection.append(obj['_id'])
        obj_ids_collection = list(set(obj_ids_collection))
        # delete keys
        for obj_id in obj_ids_collection:
            if obj_id not in serialized_objects:
                board_collection.delete_one({'_id': obj_id})
        # update and add keys
        updated_count = 0
        for obj_id, obj_repr in serialized_objects.items():
            new_data = obj_repr
            if board_collection.find_one({'_id': obj_id}) is not None:
                board_collection.update_one({'_id': obj_id}, {'$set': new_data})
            else:
                new_data['_id'] = obj_id
                board_collection.insert_one(new_data)
            updated_count += 1
        logging.debug('updated objects=%d', updated_count)

    async def start_room(self, room: YRoom):
        await super().start_room(room)
        room_name = self.get_room_name(room)[1:]
        logging.debug('room=%s started', room_name)
        self.update_ymap_from_database(room)
        logging.debug('successfully updated collections')

    def delete_room(self, *, name: str | None = None, room: YRoom | None = None) -> None:
        try:
            if room:
                room_name = self.get_room_name(room)[1:]
                logging.debug('room=%s deleting', room_name)
                self.update_database_from_ymap(room)
                logging.debug('database updated')
        except Exception as ex:
            logging.error('exception=%s from delete room came', ex)
        try:
            if room:
                super().delete_room(room=room)
            elif name:
                super().delete_room(name=name)
        except Exception as ex:
            logging.error('unexpected exception=%s from delete room came', ex)

