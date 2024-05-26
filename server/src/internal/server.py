import asyncio
import logging
import os
from typing import Mapping, Any

from pymongo import MongoClient
from pymongo.database import Database
from websockets import serve

from .websocket_server import WebsocketServerWithDB

_MONGO_URI_NO_DB = os.environ.get('MONGO_URI_NO_DB')
_OBJECTS_DB_NAME = os.environ.get('OBJECT_DB_NAME', 'boards')

_SERVER_HOST = os.environ.get('SERVER_HOST', '127.0.0.1')
_SERVER_PORT = os.environ.get('SERVER_PORT', 5000)

_RECONNECTION_TIME = int(os.environ.get('RECONNECTION_TIME', 1))
_SERVER_WAIT_START_TIME = int(os.environ.get('SERVER_WAIT_START_TIME', 1))


class WhiteBoardServer:
    _client: MongoClient[Mapping[str, Any]]
    _db: Database[Mapping[str, Any]]

    def __init__(self):
        self._client: MongoClient[Mapping[str, Any]] = MongoClient(_MONGO_URI_NO_DB)
        self._db: Database[Mapping[str, Any]] = self._client[_OBJECTS_DB_NAME]

    async def serve(self):
        while True:
            try:
                logging.debug('trying to start server')
                async with (
                    WebsocketServerWithDB(self._db) as websocket_server,
                    serve(websocket_server.serve, _SERVER_HOST, _SERVER_PORT),  # type: ignore
                ):
                    while not websocket_server.started:
                        await asyncio.sleep(_SERVER_WAIT_START_TIME)
                    logging.debug('server started')
                    await asyncio.Future()
            except Exception as ex:
                logging.debug('Exception came from server=%s', ex)
                await asyncio.sleep(_RECONNECTION_TIME)
