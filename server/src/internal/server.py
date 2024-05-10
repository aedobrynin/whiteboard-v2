import asyncio
import logging
import os
from typing import Mapping, Any

from pymongo import MongoClient
from pymongo.database import Database
from websockets import serve

from .websocket_server import WebsocketServerWithDB

# TODO: add .env file
_MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
_MONGO_PORT = os.environ.get('MONGO_PORT', 27017)

_SERVER_HOST = os.environ.get('SERVER_HOST', 'localhost')
_SERVER_PORT = os.environ.get('SERVER_PORT', 50)

_OBJECTS_DB_NAME = 'boards'


class WhiteBoardServer:
    _client: MongoClient[Mapping[str, Any]]
    _db: Database[Mapping[str, Any]]

    def __init__(self):
        self._client: MongoClient[Mapping[str, Any]] = MongoClient(f'mongodb://{_MONGO_HOST}:{_MONGO_PORT}')
        self._db: Database[Mapping[str, Any]] = self._client[_OBJECTS_DB_NAME]

    async def serve(self):
        logging.debug('trying to start server')
        async with (
            WebsocketServerWithDB(self._db) as websocket_server,
            serve(websocket_server.serve, _SERVER_HOST, _SERVER_PORT),  # type: ignore
        ):
            while not websocket_server.started:
                await asyncio.sleep(0)
            logging.debug('server started')
            await asyncio.Future()
