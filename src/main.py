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
import internal.view.view

_logging_choice_to_loglevel = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
}

RECONNECTION_TIME_SEC = 1


async def get_updates(
    shared_storage: internal.storages.impl.SharedYDocStorage,
    controller: internal.controller.impl.Controller,
    repo: internal.repositories.impl.Repository
):
    while True:
        try:
            for update in shared_storage.get_updates():
                logging.debug('SOME UPDATE: %s', update)
                obj_id = update['obj_id']
                action_type = update['obj_action']
                if action_type in ('add', 'update') and repo.get(obj_id) is None:
                    obj_repr = update['obj_repr']
                    controller.create_object_from_serialize(obj_repr)
                elif action_type == 'update':
                    obj_repr = update['obj_repr']
                    data_object_type = internal.objects.BoardObjectType(update['obj_repr']['type'])
                    if data_object_type == internal.objects.BoardObjectType.TEXT:
                        obj: internal.objects.interfaces.IBoardObjectText = repo.get(obj_id)
                        if 'position' in obj_repr:
                            position = internal.models.Position.from_serialized(obj_repr['position'])
                            if position != obj.position:
                                controller.move_object(obj.id, position - obj.position)
                        elif 'font' in obj_repr:
                            font = internal.models.Font.from_serialized(obj_repr['font'])
                            if font != obj.font:
                                controller.edit_font(obj.id, font)
                        elif 'text' in obj_repr and obj.text != obj_repr['text']:
                            controller.edit_text(obj.id, obj_repr['text'])
                        else:
                            logging.debug('the other repr %s', obj_repr)
                elif action_type == 'delete':
                    if repo.get(obj_id) is None:
                        continue
                    pass
                else:
                    logging.warning('new action type %s', action_type)
            await asyncio.sleep(0.01)
        except Exception as ex:
            logging.error('some exception in get_updates: error=%s', ex)


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
        controller=controller,
        repo=repo,
        pub_sub=broker,
        board_name=board_name
    )

    logging.debug('run client connection, get updates from server and tkinter UI update')
    await asyncio.gather(
        client_connection_handler(storage),
        get_updates(storage, controller, repo),
        internal.view.view.root_update(view)
    )


if __name__ == '__main__':
    asyncio.run(main())
