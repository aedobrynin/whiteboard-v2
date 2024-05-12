import logging
import typing

import internal.models
import internal.objects
import internal.objects.interfaces
import internal.pub_sub.interfaces
import internal.repositories.interfaces
import internal.storages.interfaces
import internal.undo_redo.interfaces

from .. import interfaces
from .edit_action import EditAction

# TODO: get rid of boilerplate code (edit_... methods looks almost the same)


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
            _obj_id: typing.Optional[internal.objects.interfaces.ObjectId]

            def __init__(
                self, controller: Controller, type: internal.objects.BoardObjectType, **kwargs
            ):
                self._controller = controller
                self._type = type
                self._kwargs = kwargs

            def do(self):
                # TODO: remember representation of created object
                # `create(1) -> undo -> redo(2)`
                # objects which were created on (1) and (2) should have the same id and representation
                logging.debug('creating object with type=%s and kwargs=%s', type, kwargs)
                obj = internal.objects.build_by_type(
                    self._type, self._controller._pub_sub_broker, **self._kwargs
                )
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
                    logging.warning('Trying to undo DeeteObjectAction with serialized_obj=None')
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
        action = EditAction(self, obj_id, 'text', text)   # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_color(self, obj_id: internal.objects.interfaces.ObjectId, color: str):
        action = EditAction(self, obj_id, 'color', color)   # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_font(self, obj_id: internal.objects.interfaces.ObjectId, font: internal.models.Font):
        action = EditAction(self, obj_id, 'font', font)   # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def _build_move_object_action(self,  obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position) -> internal.models.IAction:
        class MoveObjectAction(internal.models.IAction):
            _controller: Controller
            _obj_id: typing.Optional[internal.objects.interfaces.ObjectId]
            _delta: internal.models.Position

            def __init__(self, obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position):
                
    def move_object(
        self, obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position
    ):
        

        # TODO: undo-redo
        obj: typing.Optional[internal.objects.interfaces.IBoardObjectWithPosition] = self._repo.get(
            object_id=obj_id
        )
        if not obj:
            logging.debug('no object id=%s found to edit with delta=%s', obj_id, delta)
            return
        logging.debug('editing object with new delta=%s', delta)
        obj.position = obj.position + delta
        self._on_feature_finish()

    def edit_points(
        self,
        obj_id: internal.objects.interfaces.ObjectId,
        points: typing.List[internal.models.Position],
    ):
        action = EditAction(self, obj_id, 'points', points)   # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_children_ids(
        self,
        obj_id: internal.objects.interfaces.ObjectId,
        children_ids: typing.Tuple[internal.objects.interfaces.ObjectId],
    ):
        action = EditAction(
            self, obj_id, 'children_ids', children_ids
        )   # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def edit_width(self, obj_id: internal.objects.interfaces.ObjectId, width: float):
        action = EditAction(self, obj_id, 'width', points)   # TODO: property names as consts
        action.do()
        self._undo_redo_manager.store_action(action)

    def undo_last_action(self):
        logging.debug('controller was asked to undo last action')
        self._undo_redo_manager.undo()

    def redo_last_action(self):
        logging.debug('controller was asked to redo last action')
        self._undo_redo_manager.redo()
