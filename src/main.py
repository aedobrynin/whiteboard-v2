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


async def get_updates(
    shared_storage: internal.storages.impl.SharedYDocStorage,
    controller: internal.controller.impl.Controller,
    repo: internal.repositories.impl.Repository,
    stop: asyncio.Event
):
    while not stop.is_set():
        try:
            for update in shared_storage.get_updates():
                obj_id = update['obj_id']
                action_type = update['obj_action']
                if action_type in ('add', 'update') and repo.get(obj_id) is None:
                    obj_repr = update['obj_repr']
                    controller.create_object_from_serialize(obj_repr)
                elif action_type == 'update':
                    obj_repr = update['obj_repr']
                    obj: internal.objects.interfaces.IBoardObject = repo.get(obj_id)
                    if 'position' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectWithPosition
                    ):
                        position = internal.models.Position.from_serialized(obj_repr['position'])
                        if position != obj.position:
                            controller.move_object(obj.id, position - obj.position)
                    if 'font' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectWithFont
                    ):
                        font = internal.models.Font.from_serialized(obj_repr['font'])
                        if font != obj.font:
                            controller.edit_font(obj.id, font)
                    if 'text' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectWithFont
                    ) and obj.text != obj_repr['text']:
                        controller.edit_text(obj.id, obj_repr['text'])
                    if 'color' in obj_repr and isinstance(
                        obj, (
                            internal.objects.interfaces.IBoardObjectPen,
                            internal.objects.interfaces.IBoardObjectCard,
                            internal.objects.interfaces.IBoardObjectConnector
                        )
                    ) and obj.color != obj_repr['color']:
                        controller.edit_color(obj.id, obj_repr['color'])
                    if 'points' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectPen
                    ) and obj.points != obj_repr['points']:
                        points = [internal.models.Position.from_serialized(point) for point in obj_repr['points']]
                        controller.edit_points(obj.id, points)
                    if 'children_ids' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectGroup
                    ) and obj.children_ids != obj_repr['children_ids']:
                        controller.edit_children_ids(obj.id, obj_repr['children_ids'])
                    if 'connector_type' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectConnector
                    ) and obj.connector_type != obj_repr['connector_type']:
                        controller.edit_connector_type(obj.id, obj_repr['connector_type'])
                    if 'stroke_style' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectConnector
                    ) and obj.stroke_style != obj_repr['stroke_style']:
                        controller.edit_stroke_style(obj.id, obj_repr['stroke_style'])
                    if 'width' in obj_repr and isinstance(
                        obj, (
                            internal.objects.interfaces.IBoardObjectPen,
                            internal.objects.interfaces.IBoardObjectCard,
                            internal.objects.interfaces.IBoardObjectConnector,
                        )
                    ) and obj.width != obj_repr['width']:
                        controller.edit_width(obj.id, obj_repr['width'])
                    if 'height' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectCard
                    ) and obj.height != obj_repr['height']:
                        controller.edit_height(obj.id, obj_repr['height'])
                    if ('columns_width' in obj_repr or 'rows_height' in obj_repr) and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectTable
                    ):
                        if 'columns_width' in obj_repr and 'rows_height' in obj_repr and (
                            obj.columns_width != obj_repr['columns_width'] or
                            obj.rows_height != obj_repr['rows_height']
                        ):
                            controller.edit_table(
                                obj.id, obj_repr['columns_width'], obj_repr['rows_height']
                            )
                        if 'columns_width' in obj_repr and obj.columns_width != obj_repr[
                            'columns_width'
                        ]:
                            controller.edit_table(
                                obj.id, obj_repr['columns_width'], obj.rows_height
                            )
                        if 'rows_height' in obj_repr and obj.rows_height != obj_repr[
                            'rows_height'
                        ]:
                            controller.edit_table(
                                obj.id, obj.columns_width, obj_repr['rows_height']
                            )
                    if 'linked_objects' in obj_repr and isinstance(
                        obj, internal.objects.interfaces.IBoardObjectCard
                    ) and obj.linked_objects != obj_repr['linked_objects']:
                        controller.edit_linked_objects(obj.id, obj_repr['linked_objects'])
                elif action_type == 'delete':
                    if repo.get(obj_id) is None:
                        continue
                    controller.delete_object(obj_id)
                else:
                    logging.warning('new action type %s', action_type)
            await asyncio.sleep(0.01)
        except Exception as ex:
            logging.error('some exception in get_updates: error=%s', ex)


async def client_connection_handler(
    shared_storage: internal.storages.impl.SharedYDocStorage, stop: asyncio.Event
):
    while not stop.is_set():
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


async def create_tasks(tasks):
    # Server and get_update never falls because of future and while, only tk can fall
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


async def main():
    parser = argparse.ArgumentParser()

    # board_name, board_key = get_board_name_key()
    board_name, board_key = "Whiteboard", "board"

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
        controller=controller,
        repo=repo,
        pub_sub=broker,
        board_name=board_name
    )

    logging.debug('run client connection, get updates from server and tkinter UI update')
    stop = asyncio.Event()
    await create_tasks([
        asyncio.create_task(client_connection_handler(storage, stop)),
        asyncio.create_task(get_updates(storage, controller, repo, stop)),
        asyncio.create_task(internal.view.view.root_update(view, stop))
    ])


if __name__ == '__main__':
    asyncio.run(main())
