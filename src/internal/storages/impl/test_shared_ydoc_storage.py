import asyncio
import logging

import pytest
from websockets import connect, serve  # type: ignore
from ypy_websocket import WebsocketServer

from . import LocalYDocStorage
from .shared_ydoc_storage import SharedYDocStorage, SERVER_PORT


@pytest.mark.asyncio
async def test_shared_ydoc_storage_get_updates():
    logging.info('START')
    board_name = 'test-board'
    updates = {
        'obj_id_1': {'a1': 'b1'},
        'obj_id_2': {'a2': 'b2'},
        'obj_id_3': {'a3': 'b3'},
        'obj_id_4': {'a4': 'b4'}
    }
    # client 1
    storage_1 = SharedYDocStorage(board_name)
    storage_1.update(updates)
    assert storage_1.get_serialized_objects() == updates
    assert not storage_1.is_empty_updates()  # !!!! no connection to server

    # async with (
    #     WebsocketServer(auto_clean_rooms=False) as websocket_server,
    #     serve(websocket_server.serve, 'localhost', SERVER_PORT)  # type: ignore
    # ):
    #     while not websocket_server.started:
    #         await asyncio.sleep(0)

    logging.debug('try to connect to server=%s...', storage_1.get_uri_connection())
    async with connect(storage_1.get_uri_connection()) as websocket:
        logging.info('successfully connected to server')
        async with storage_1.get_websocket_provider(websocket):  # type: ignore
            await asyncio.sleep(1)
    assert not storage_1.is_empty_updates()
    for k, v in storage_1.get_updates():
        logging.info('assert v(%s) = update[k](%s)', v, updates[k])
        assert v == updates[k]

    # client 2
    storage_2 = SharedYDocStorage(board_name)
    assert storage_2.is_empty_updates()
    async with connect(storage_2.get_uri_connection()) as websocket:
        logging.info('successfully connected to server')
        async with storage_2.get_websocket_provider(websocket):  # type: ignore
            await asyncio.sleep(1)

    assert not storage_2.is_empty_updates()
    for k, v in storage_2.get_updates():
        logging.info('assert v(%s) = update[k](%s)', v, updates[k])
        assert v == updates[k]


@pytest.mark.asyncio
async def test_shared_ydoc_storage_x_local_storage(tmp_path):
    logging.info('START')
    board_name = 'test-board'
    # local
    path = tmp_path / 'storage'
    storage_local = LocalYDocStorage(path)
    updates = {
        'obj_id_1': {'a1': 'b1'},
        'obj_id_2': {'a2': 'b2'},
        'obj_id_3': {'a3': 'b3'},
        'obj_id_4': {'a4': 'b4'}
    }
    storage_local.update(updates)
    async with (
        WebsocketServer(auto_clean_rooms=False) as websocket_server,
        serve(websocket_server.serve, 'localhost', SERVER_PORT)  # type: ignore
    ):
        while not websocket_server.started:
            await asyncio.sleep(0)
        # client
        shared_storage = SharedYDocStorage(board_name)
        async with connect(shared_storage.get_uri_connection()) as websocket:
            logging.info('successfully connected to server')
            async with shared_storage.get_websocket_provider(websocket):  # type: ignore
                await asyncio.sleep(1)

        assert shared_storage.is_empty_updates()
