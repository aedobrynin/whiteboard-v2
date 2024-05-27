from __future__ import annotations

import logging
from datetime import datetime

from pymongo.database import Database, Mapping, Any
from ypy_websocket import WebsocketServer, YRoom

_Y_DOC_OBJECTS_FIELD_NAME = 'objects'


class WebsocketServerWithDB(WebsocketServer):
    _db: Database[Mapping[str, Any]]

    def __init__(self, db: Database[Mapping[str, Any]]):
        WebsocketServer.__init__(self)
        self._db = db

    def update_ymap_from_database(self, room: YRoom):
        logging.debug('loading collection')
        room_name = self.get_room_name(room)[1:]
        board_collection = self._db['table_' + room_name]
        logging.debug('successfully loaded collection')
        doc_ymap = room.ydoc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)
        updated_count = 0
        objects: dict[str, dict] = dict()
        for obj in board_collection.find():
            obj_repr = dict(obj)
            obj_id = obj_repr.pop('_id')
            objects[obj_id] = obj_repr
        for obj_id in sorted(
            objects,
            key=lambda _id: datetime.strptime(objects[_id]['create_dttm'], '%Y-%m-%dT%H-%M-%SZ')
        ):
            with room.ydoc.begin_transaction() as t:
                doc_ymap.set(t, obj_id, objects[obj_id])
                updated_count += 1
        logging.debug('updated objects=%d', updated_count)

    def update_database_from_ymap(self, serialized_objects: dict, board_name: str):
        logging.debug('loading collection')
        board_collection = self._db['table_' + board_name]
        logging.debug('successfully loaded collection')
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

    async def get_room(self, name: str) -> YRoom:
        if name not in self.rooms:
            self.rooms[name] = YRoom(ready=self.rooms_ready, log=self.log)
            room_name = self.get_room_name(self.rooms[name])[1:]
            logging.debug('room=%s started', room_name)
            self.update_ymap_from_database(self.rooms[name])
            logging.debug('successfully updated collections')
        room = self.rooms[name]
        await self.start_room(room)
        return self.rooms[name]

    def delete_room(self, *, name: str | None = None, room: YRoom | None = None) -> None:
        if name is not None and room is not None:
            raise RuntimeError('Cannot pass name and room')
        if name is None:
            assert room is not None
            name = self.get_room_name(room)
        logging.debug('room=%s deleting', name)
        try:
            serialized_objects = dict(self.rooms[name].ydoc.get_map(_Y_DOC_OBJECTS_FIELD_NAME))
            self.update_database_from_ymap(serialized_objects, name[1:])
            logging.debug('database updated')
        except Exception as ex:
            logging.error('exception=%s from delete room came', ex)
        room = self.rooms.pop(name)
        room.stop()
