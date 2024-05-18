import logging
import typing

import internal.models
import internal.objects
import internal.objects.interfaces
import internal.pub_sub.interfaces
import internal.repositories.interfaces
import internal.storages
import internal.storages.interfaces
import internal.undo_redo.interfaces

from .. import interfaces
from .edit_action import EditAction, PropertyChange


class Controller(interfaces.IController):
    def __init__(
        self,
        repo: internal.repositories.interfaces.IRepository,
        storage: internal.storages.interfaces.IStorage,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
        undo_redo_manager: internal.undo_redo.interfaces.IUndoRedoManager,
    ):
        self._repo = repo
        self._storage = storage
        self._pub_sub_broker = pub_sub_broker
        self._undo_redo_manager = undo_redo_manager

    # TODO: feature abstraction (IFeature)
    def _on_feature_finish(self):
        logging.debug('start executing feature finish pipeline')
        # 1) Process pub-sub
        # 2) Extract updates from repo
        # 3) Push updates to storage
        # 4) Push updates to UndoRedoManager
        # Fetch updates from storage and update repo sometimes (future work)

        logging.debug('processing published pub_sub events')
        self._pub_sub_broker.process_published(self._repo)

        logging.debug('saving updates to the storage')
        # TODO: myb better API for updates?
        updates = self._repo.get_updated()
        raw_updates: internal.storages.interfaces.IStorage.UpdatesType = {}
        for (obj_id, update) in updates.items():
            raw_updates[obj_id] = update
        self._storage.update(raw_updates)
        logging.debug('finished executing feature finish pipeline')

    def _build_create_object_action(
        self, type: internal.objects.BoardObjectType, **kwargs
    ) -> internal.models.IAction:
        class CreateObjectAction(internal.models.IAction):
            _controller: Controller
            _type: internal.objects.BoardObjectType
            _kwargs: dict
            _serialized_obj: typing.Optional[dict]
            _obj_id: typing.Optional[internal.objects.interfaces.ObjectId]

            def __init__(
                self, controller: Controller, type: internal.objects.BoardObjectType, **kwargs
            ):
                self._controller = controller
                self._type = type
                self._kwargs = kwargs
                # Myb this will be changed in the future
                # If we have sequence `create(1) -> undo -> redo(2)`
                # objects which were created on (1) and (2) should
                # have the same id in order to other redo actions to be applied successfully
                self._serialized_obj = None
                self._obj_id = None

            def do(self):
                logging.debug('creating object with type=%s and kwargs=%s', type, kwargs)
                if self._serialized_obj:
                    logging.debug(
                        'CreateObjectAction: object was created before, restore from serialized'
                    )
                    obj = internal.objects.build_from_serialized(
                        self._serialized_obj, self._controller._pub_sub_broker
                    )
                else:
                    obj = internal.objects.build_by_type(
                        self._type, self._controller._pub_sub_broker, **self._kwargs
                    )
                    self._serialized_obj = obj.serialize()
                    self._obj_id = obj.id

                self._controller._repo.add(obj)
                self._controller._on_feature_finish()

            def undo(self):
                if not self._obj_id:
                    logging.warning('Trying to undo CreateObjectAction with obj_id=None')
                    return
                action = self._controller._build_delete_object_action(self._obj_id)
                action.do()
                self._controller._on_feature_finish()

        return CreateObjectAction(self, type, **kwargs)

    def create_object(self, type: internal.objects.BoardObjectType, **kwargs):  # noqa
        action = self._build_create_object_action(type, **kwargs)
        action.do()
        self._undo_redo_manager.store_action(action)

    def _build_delete_object_action(
        self, obj_id: internal.objects.interfaces.ObjectId
    ) -> internal.models.IAction:
        class DeleteObjectAction(internal.models.IAction):
            _controller: Controller
            _obj_id: typing.Optional[internal.objects.interfaces.ObjectId]
            _serialized_obj: typing.Optional[dict]

            def __init__(
                self, controller: Controller, obj_id: internal.objects.interfaces.ObjectId
            ):
                self._controller = controller
                self._obj_id = obj_id
                self._serialized_obj = None

            def do(self):
                logging.debug('deleting object with id=%s', self._obj_id)
                obj = self._controller._repo.get(self._obj_id)
                if not obj:
                    logging.warning('no object with id=%s', self._obj_id)
                    return
                self._serialized_obj = obj.serialize()
                self._controller._repo.delete(obj_id)
                self._controller._on_feature_finish()

            def undo(self):
                if not self._serialized_obj:
                    logging.warning('Trying to undo DeleteObjectAction with serialized_obj=None')
                    return
                obj = internal.objects.build_from_serialized(
                    self._serialized_obj, self._controller._pub_sub_broker
                )
                self._controller._repo.add(obj)
                self._controller._on_feature_finish()

        return DeleteObjectAction(self, obj_id)

    def delete_object(self, obj_id: internal.objects.interfaces.ObjectId):
        action = self._build_delete_object_action(obj_id)
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_text(self, obj_id: internal.objects.interfaces.ObjectId, text: str):
        action = EditAction(
            self, obj_id, [PropertyChange('text', text)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_color(self, obj_id: internal.objects.interfaces.ObjectId, color: str):
        action = EditAction(
            self, obj_id, [PropertyChange('color', color)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_font(self, obj_id: internal.objects.interfaces.ObjectId, font: internal.models.Font):
        action = EditAction(
            self, obj_id, [PropertyChange('font', font)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def _build_move_object_action(
        self, obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position
    ) -> internal.models.IAction:
        class MoveObjectAction(internal.models.IAction):
            _controller: Controller
            _obj_id: typing.Optional[internal.objects.interfaces.ObjectId]
            _delta: internal.models.Position

            def __init__(
                self,
                controller: Controller,
                obj_id: internal.objects.interfaces.ObjectId,
                delta: internal.models.Position,
            ):
                self._controller = controller
                self._obj_id = obj_id
                self._delta = delta

            def _move_by_object(
                self, delta: internal.models.Position, obj: internal.objects.interfaces.IBoardObject
            ):
                if isinstance(obj, internal.objects.interfaces.IBoardObjectWithPosition):
                    obj.position = obj.position + delta
                elif isinstance(obj, internal.objects.interfaces.IBoardObjectPen):
                    # TODO: myb make Pen object with position?
                    points = []
                    for point in obj.points:
                        points.append(point + delta)
                    obj.points = points
                elif isinstance(obj, internal.objects.interfaces.IBoardObjectGroup):
                    for child_id in obj.children_ids:
                        child_obj = self._controller._repo.get(child_id)
                        if child_obj:
                            self._move_by_object(delta, child_obj)
                else:
                    logging.error('move is not implemented for object of type %s', obj.type)

            def _move(self, delta: internal.models.Position):
                obj: typing.Optional[
                    internal.objects.interfaces.IBoardObject
                ] = self._controller._repo.get(self._obj_id)
                if not obj:
                    logging.warning('MoveObjectAction: no object with id=%s', self._obj_id)
                    return
                self._move_by_object(delta, obj)
                self._controller._on_feature_finish()

            def do(self):
                logging.debug(
                    'trying to move object with id=%s, delta=%s', self._obj_id, self._delta
                )
                self._move(self._delta)

            def undo(self):
                logging.debug(
                    'trying to undo move action for object with id=%s, delta=%s',
                    self._obj_id,
                    self._delta,
                )
                self._move(-self._delta)

        return MoveObjectAction(self, obj_id, delta)

    def move_object(
        self, obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position
    ):
        action = self._build_move_object_action(obj_id, delta)
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_points(
        self, obj_id: internal.objects.interfaces.ObjectId,
        points: typing.List[internal.models.Position],
    ):
        action = EditAction(
            self, obj_id, [PropertyChange('points', points)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_connector_type(
        self, obj_id: internal.objects.interfaces.ObjectId, connector_type: str
    ):
        action = EditAction(
            self, obj_id, [PropertyChange('connector_type', connector_type)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_stroke_style(
        self, obj_id: internal.objects.interfaces.ObjectId, stroke_style: str
    ):
        action = EditAction(
            self, obj_id, [PropertyChange('stroke_style', stroke_style)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_width(self, obj_id: internal.objects.interfaces.ObjectId, width: int):
        action = EditAction(
            self, obj_id, [PropertyChange('width', width)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_height(self, obj_id: internal.objects.interfaces.ObjectId, height: int):
        action = EditAction(
            self, obj_id, [PropertyChange('height', height)]
        )  # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_size(self, obj_id: internal.objects.interfaces.ObjectId, width: int, height: int):
        action = EditAction(
            self,
            obj_id,
            [
                PropertyChange('width', width),
                PropertyChange('height', height),
            ],
        )
        action.do()
        self._undo_redo_manager.store_action(action)

    def undo_last_action(self):
        logging.debug('controller was asked to undo last action')
        self._undo_redo_manager.undo()

    def redo_last_action(self):
        logging.debug('controller was asked to redo last action')
        self._undo_redo_manager.redo()
