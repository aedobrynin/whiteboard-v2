import argparse
import asyncio
import logging

from websockets import connect, ConnectionClosed

import internal.controller.impl
import internal.models
import internal.objects
import internal.objects.interfaces
import internal.pub_sub.impl
import internal.repositories.impl
import internal.storages.impl
import internal.undo_redo.impl
import internal.view.choose_board
import internal.view.view

_logging_choice_to_loglevel = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
}

RECONNECTION_TIME_SEC = 1


async def client_connection_handler(
    shared_storage: internal.storages.impl.SharedYDocStorage, stop: asyncio.Event
):
    while not stop.is_set():
        logging.debug('trying to connect to server=%s...', shared_storage.get_uri_connection())
        try:
            async with (
                connect(shared_storage.get_uri_connection()) as websocket,
                shared_storage.get_websocket_provider(websocket),  # type: ignore
            ):
                logging.info('successfully connected to server')
                await asyncio.Future()
        except ConnectionClosed:
            logging.debug('connection to server closed... trying to reconnect...')
            await asyncio.sleep(RECONNECTION_TIME_SEC)
        except Exception as ex:
            logging.error('some exception in websocket connect: error=%s', ex)
            await asyncio.sleep(RECONNECTION_TIME_SEC)


async def create_tasks(tasks):
    # Server and get_update never falls because of future and while, only tk can fall
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


async def main():
    parser = argparse.ArgumentParser()

    # board_name, board_key = get_board_name_key()
    board_name, board_key = 'Whiteboard', 'board'

    parser.add_argument(
        'board-name',
        type=str,
        help='server board name',
        nargs='?',
        default='sample_board',
    )

    parser.add_argument(
        'logging-level',
        type=str,
        help='logging level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        nargs='?',
        default='DEBUG',
    )
    args = vars(parser.parse_args())

    logging.basicConfig(
        level=_logging_choice_to_loglevel[args['logging-level']],
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    logging.debug('initializing pubsub broker')
    broker = internal.pub_sub.impl.PubSubBroker()
    logging.debug('initializing storage')
    storage = internal.storages.impl.SharedYDocStorage(board_name, board_key)
    serialized_objects = storage.get_serialized_objects()
    objects = []
    for serialized_obj in serialized_objects.values():
        objects.append(internal.objects.build_from_serialized(serialized_obj, broker))
    logging.info('successfully parsed all objects from storage')

    logging.debug('initializing repo')
    repo = internal.repositories.impl.Repository(objects, broker)

    logging.debug('clearing created pub-sub events')
    broker.clear_events()

    undo_redo_manager_max_history_size = 100  # TODO: move to cfg
    logging.debug(
        'initializing undo-redo manager with max_history_size=%d',
        undo_redo_manager_max_history_size,
    )
    undo_redo_manager = internal.undo_redo.impl.UndoRedoManager(undo_redo_manager_max_history_size)

    logging.debug('initializing controller')
    controller = internal.controller.impl.Controller(repo, storage, broker, undo_redo_manager)

    logging.debug('initializing tkinter')
    view = internal.view.view.create_view(
        controller=controller, repo=repo, pub_sub=broker, board_name=board_name
    )

    logging.debug('run client connection, get updates from server and tkinter UI update')
    stop = asyncio.Event()
    await create_tasks(
        [
            asyncio.create_task(client_connection_handler(storage, stop)),
            asyncio.create_task(storage.run(controller, repo, stop)),
            asyncio.create_task(internal.view.view.root_update(view, stop)),
        ]
    )


if __name__ == '__main__':
    asyncio.run(main())
