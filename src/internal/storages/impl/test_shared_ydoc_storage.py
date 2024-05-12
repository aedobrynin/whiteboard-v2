import asyncio
import logging

import pytest
from websockets import connect, serve  # type: ignore
from ypy_websocket import WebsocketServer

from .shared_ydoc_storage import SharedYDocStorage, SERVER_PORT


@pytest.mark.asincio
async def test_shared_ydoc_storage_get_updates():
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

    async with (
        WebsocketServer(auto_clean_rooms=False) as websocket_server,
        serve(websocket_server.serve, 'localhost', SERVER_PORT)  # type: ignore
    ):
        while not websocket_server.started:
            await asyncio.sleep(0)

        async with connect(storage_1.get_uri_connection()) as websocket:
            async with storage_1.get_websocket_provider(websocket):  # type: ignore
                await asyncio.sleep(1)
        assert not storage_1.is_empty_updates()
        for obj in storage_1.get_updates():
            assert obj['obj_repr'] == updates[obj['obj_id']]

        # client 2
        storage_2 = SharedYDocStorage(board_name)
        assert storage_2.is_empty_updates()
        async with connect(storage_2.get_uri_connection()) as websocket:
            async with storage_2.get_websocket_provider(websocket):  # type: ignore
                await asyncio.sleep(1)

        assert not storage_2.is_empty_updates()
        for obj in storage_2.get_updates():
            assert obj['obj_repr'] == updates[obj['obj_id']]
