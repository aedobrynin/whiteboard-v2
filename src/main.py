import argparse
import asyncio
import logging
import pathlib
import tkinter

from websockets import connect, ConnectionClosed

import internal.controller.impl
import internal.objects
import internal.objects
import internal.pub_sub.impl
import internal.repositories.impl
import internal.storages.impl
import internal.view.view

_logging_choice_to_loglevel = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
}

RECONNECTION_TIME_SEC = 1

connection_closed = False


async def root_update(
    view: tkinter.Tk
):
    while True:
        try:
            view.update()
            await asyncio.sleep(0)
        except Exception as ex:
            logging.error('some exception in tkinter: error=%s', ex)


async def get_updates(
    shared_storage: internal.storages.impl.SharedYDocStorage,
    controller: internal.controller.impl.Controller,
    repo: internal.repositories.impl.Repository
):
    while True:
        try:
            for update in shared_storage.get_updates():
                obj_id = update[0]
                obj = dict(update[1])
                type = obj['type']
                logging.debug('SOME UPDATE: %s', obj)
            await asyncio.sleep(0)
        except Exception as ex:
            logging.error('some exception in get_updates: error=%s', ex)


def run_loop_connection(
    loop: asyncio.AbstractEventLoop,
    shared_storage: internal.storages.impl.SharedYDocStorage
):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client_connection_handler(shared_storage))
    loop.close()


async def client_connection_handler(
    shared_storage: internal.storages.impl.SharedYDocStorage
):
    while True:
        logging.debug('trying to connect to server=%s...', shared_storage.get_uri_connection())
        try:
            async with (
                connect(shared_storage.get_uri_connection()) as websocket,
                shared_storage.get_websocket_provider(websocket)  # type: ignore
            ):
                logging.info('successfully connected to server')
                await asyncio.Future()
        except ConnectionClosed:
            logging.debug('connection to server closed... trying to reconnect...')
            await asyncio.sleep(RECONNECTION_TIME_SEC)
        except Exception as ex:
            logging.error('some exception in websocket connect: error=%s', ex)
            await asyncio.sleep(RECONNECTION_TIME_SEC)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'board-path',
        type=pathlib.Path,
        help='path to board',
        nargs='?',
        default='storage.boardobj',
    )

    parser.add_argument(
        'board-name',
        type=pathlib.Path,
        help='server board key',
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
    board_name = args['board-name']

    logging.debug('initializing pubsub broker')
    broker = internal.pub_sub.impl.PubSubBroker()
    logging.debug('initializing storage')
    storage = internal.storages.impl.SharedYDocStorage(board_name)
    serialized_objects = storage.get_serialized_objects()
    objects = []
    for serialized_obj in serialized_objects.values():
        objects.append(internal.objects.build_from_serialized(serialized_obj, broker))
    logging.info('successfully parsed all objects from storage')

    logging.debug('initializing repo')
    repo = internal.repositories.impl.Repository(objects, broker)

    logging.debug('initializing controller')
    controller = internal.controller.impl.Controller(repo, storage, broker)

    logging.debug('initializing tkinter')

    view = internal.view.view.create_view(
        controller=controller,
        repo=repo,
        pub_sub=broker
    )
    await asyncio.gather(
        client_connection_handler(storage),
        get_updates(storage, controller),
        root_update(view)
    )


if __name__ == '__main__':
    asyncio.run(main())
