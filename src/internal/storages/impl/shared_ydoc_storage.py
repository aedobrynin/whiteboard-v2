import os
import queue
import logging

import asyncio
from y_py import YMapEvent
from ypy_websocket import WebsocketProvider
from ypy_websocket.websocket import Websocket

from .ydoc_storage import YDocStorage, _Y_DOC_OBJECTS_FIELD_NAME
from .. import interfaces
import internal.controller.interfaces
import internal.repositories.interfaces

# TODO: .env file
SERVER_HOST = os.environ.get('SERVER_HOST', '51.250.90.146')
SERVER_PORT = os.environ.get('SERVER_PORT', 8080)
URI_WEBSOCKET_SERVER = f'ws://{SERVER_HOST}:{SERVER_PORT}'


class SharedYDocStorage(YDocStorage, interfaces.ISharedStorage):
    def __init__(self, board_name: str, board_key: str):
        YDocStorage.__init__(self)
        self._board_name = board_name
        self._board_key = board_key
        self._cur_changes = queue.Queue()

        self._doc_ymap = self._y_doc.get_map(_Y_DOC_OBJECTS_FIELD_NAME)
        self._obj_updates_subscription_id = self._doc_ymap.observe(self._transaction_callback_obj)

    def get_uri_connection(self):
        return f'{URI_WEBSOCKET_SERVER}/{self._board_key}'

    def get_websocket_provider(self, websocket: Websocket):
        return WebsocketProvider(self._y_doc, websocket)

    def _transaction_callback_obj(self, event: YMapEvent):
        for obj_id, change in event.keys.items():
            obj = dict()
            obj['obj_repr'] = change['newValue'] if change['action'] != 'delete' else None
            obj['obj_action'] = change['action']
            obj['obj_id'] = obj_id
            self._cur_changes.put(obj)

    # TODO: удалить?
    def is_empty_updates(self):
        return self._cur_changes.empty()

    def _get_updates(self) -> dict:
        while not self._cur_changes.empty():
            yield self._cur_changes.get()

    # TODO: перестать принимать контроллер и обновлять объекты через его вызовы
    async def run(
        self,
        controller: internal.controller.interfaces.IController,
        repo: internal.repositories.interfaces.IRepository,
        stop: asyncio.Event,
    ):
        while not stop.is_set():
            try:
                for update in self._get_updates():
                    assert self._obj_updates_subscription_id is not None
                    self._doc_ymap.unobserve(self._obj_updates_subscription_id)
                    self._obj_updates_subscription_id = None

                    # TODO: переделать на унифицированный механизм
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
                            position = internal.models.Position.from_serialized(
                                obj_repr['position']
                            )
                            if position != obj.position:
                                controller.move_object(obj.id, position - obj.position)
                        if 'font' in obj_repr and isinstance(
                            obj, internal.objects.interfaces.IBoardObjectWithFont
                        ):
                            font = internal.models.Font.from_serialized(obj_repr['font'])
                            if font != obj.font:
                                controller.edit_font(obj.id, font)
                        if (
                            'text' in obj_repr
                            and isinstance(obj, internal.objects.interfaces.IBoardObjectWithFont)
                            and obj.text != obj_repr['text']
                        ):
                            controller.edit_text(obj.id, obj_repr['text'])
                        if (
                            'color' in obj_repr
                            and isinstance(
                                obj,
                                (
                                    internal.objects.interfaces.IBoardObjectPen,
                                    internal.objects.interfaces.IBoardObjectCard,
                                    internal.objects.interfaces.IBoardObjectConnector,
                                ),
                            )
                            and obj.color != obj_repr['color']
                        ):
                            controller.edit_color(obj.id, obj_repr['color'])
                        if (
                            'points' in obj_repr
                            and isinstance(obj, internal.objects.interfaces.IBoardObjectPen)
                            and obj.points != obj_repr['points']
                        ):
                            points = [
                                internal.models.Position.from_serialized(point)
                                for point in obj_repr['points']
                            ]
                            controller.edit_points(obj.id, points)
                        if (
                            'children_ids' in obj_repr
                            and isinstance(obj, internal.objects.interfaces.IBoardObjectGroup)
                            and obj.children_ids != obj_repr['children_ids']
                        ):
                            controller.edit_children_ids(obj.id, obj_repr['children_ids'])
                        if (
                            'connector_type' in obj_repr
                            and isinstance(obj, internal.objects.interfaces.IBoardObjectConnector)
                            and obj.connector_type != obj_repr['connector_type']
                        ):
                            controller.edit_connector_type(obj.id, obj_repr['connector_type'])
                        if (
                            'stroke_style' in obj_repr
                            and isinstance(obj, internal.objects.interfaces.IBoardObjectConnector)
                            and obj.stroke_style != obj_repr['stroke_style']
                        ):
                            controller.edit_stroke_style(obj.id, obj_repr['stroke_style'])
                        if (
                            'width' in obj_repr
                            and isinstance(
                                obj,
                                (
                                    internal.objects.interfaces.IBoardObjectPen,
                                    internal.objects.interfaces.IBoardObjectCard,
                                    internal.objects.interfaces.IBoardObjectConnector,
                                ),
                            )
                            and obj.width != obj_repr['width']
                        ):
                            controller.edit_width(obj.id, obj_repr['width'])
                        if (
                            'height' in obj_repr
                            and isinstance(obj, internal.objects.interfaces.IBoardObjectCard)
                            and obj.height != obj_repr['height']
                        ):
                            controller.edit_height(obj.id, obj_repr['height'])
                        if (
                            'columns_width' in obj_repr or 'rows_height' in obj_repr
                        ) and isinstance(obj, internal.objects.interfaces.IBoardObjectTable):
                            if (
                                'columns_width' in obj_repr
                                and 'rows_height' in obj_repr
                                and (
                                    obj.columns_width != obj_repr['columns_width']
                                    or obj.rows_height != obj_repr['rows_height']
                                )
                            ):
                                controller.edit_table(
                                    obj.id, obj_repr['columns_width'], obj_repr['rows_height']
                                )
                            if (
                                'columns_width' in obj_repr
                                and obj.columns_width != obj_repr['columns_width']
                            ):
                                controller.edit_table(
                                    obj.id, obj_repr['columns_width'], obj.rows_height
                                )
                            if (
                                'rows_height' in obj_repr
                                and obj.rows_height != obj_repr['rows_height']
                            ):
                                controller.edit_table(
                                    obj.id, obj.columns_width, obj_repr['rows_height']
                                )
                        if (
                            'linked_objects' in obj_repr
                            and isinstance(obj, internal.objects.interfaces.IBoardObjectCard)
                            and obj.linked_objects != obj_repr['linked_objects']
                        ):
                            controller.edit_linked_objects(obj.id, obj_repr['linked_objects'])
                    elif action_type == 'delete':
                        if repo.get(obj_id) is None:
                            continue
                        controller.delete_object(obj_id)
                    else:
                        logging.warning('new action type %s', action_type)

                self._obj_updates_subscription_id = self._doc_ymap.observe(
                    self._transaction_callback_obj
                )
                await asyncio.sleep(0.01)
            except Exception as ex:
                logging.error('some exception in get_updates: error=%s', ex)
