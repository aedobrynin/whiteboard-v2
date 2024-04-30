import logging
import typing

import internal.models
import internal.objects
import internal.objects.interfaces
import internal.pub_sub.interfaces
import internal.repositories.interfaces
import internal.storages

from .. import interfaces


class Controller(interfaces.IController):
    def __init__(
        self,
        repo: internal.repositories.interfaces.IRepository,
        storage: internal.storages.interfaces.IStorage,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ):
        self._repo = repo
        self._storage = storage
        self._pub_sub_broker = pub_sub_broker

    # TODO: feature abstraction
    def _on_feature_finish(self):
        logging.debug('start executing feature finish pipeline')
        # 1) Process pub-sub
        # 2) Extract updates from repo
        # 3) Push updates to storage
        # 4) Push updates to UndoRedoManager (future work)
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

    def create_object(
        self, type: internal.objects.BoardObjectType, position: internal.models.Position  # noqa
    ):
        logging.debug('creating object with type=%s, position=%s', type, position)
        obj = internal.objects.build_by_type(type, position, self._pub_sub_broker)
        self._repo.add(obj)
        self._on_feature_finish()

    def delete_object(
        self, obj_id: internal.objects.interfaces.ObjectId
    ):
        logging.debug('deleting object=%s', obj_id)
        self._repo.delete(obj_id)
        self._on_feature_finish()

    def edit_focus(
        self, obj_id: internal.objects.interfaces.ObjectId, focus: bool
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithPosition
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing focus of object from=%s, to=%s ',
                obj.focus,
                focus
            )
            obj.focus = focus
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit focus=%s', obj_id, focus)

    def edit_text(
        self, obj_id: internal.objects.interfaces.ObjectId, text: str
    ):
        obj: typing.Union[
            internal.objects.interfaces.IBoardObjectCard,
            internal.objects.interfaces.IBoardObjectText,
            None
        ] = self._repo.get(object_id=obj_id)
        # TODO: think about incorrect obj type
        if obj:
            logging.debug('editing text of object old text=%s, new text=%s ', obj.text, text)
            obj.text = text
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with text=%s', obj_id, text)

    def edit_font_color(
        self, obj_id: internal.objects.interfaces.ObjectId, color: str
    ):
        obj: typing.Union[
            internal.objects.interfaces.IBoardObjectCard,
            internal.objects.interfaces.IBoardObjectText,
            None
        ] = self._repo.get(object_id=obj_id)
        # TODO: think about incorrect obj type
        if obj:
            logging.debug('editing font color of object old color=%s, new color=%s ',
                          obj.font_color, color)
            obj.font_color = color
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with text=%s', obj_id, color)

    def move_object(
        self, obj_id: internal.objects.interfaces.ObjectId, position: internal.models.Position
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithPosition
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing coord of object old coord=%s, new coord=%s ',
                obj.position,
                position
            )
            obj.position = position
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with position=%s', obj_id, position)
