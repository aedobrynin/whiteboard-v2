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
        self, type: internal.objects.BoardObjectType, **kwargs  # noqa
    ):
        logging.debug('creating object with type=%s and kwargs=%s', type, kwargs)
        obj = internal.objects.build_by_type(type, self._pub_sub_broker, **kwargs)
        self._repo.add(obj)
        self._on_feature_finish()

    def delete_object(
        self, obj_id: internal.objects.interfaces.ObjectId
    ):
        logging.debug('deleting object=%s', obj_id)
        self._repo.delete(obj_id)
        self._on_feature_finish()

    def edit_text(
        self, obj_id: internal.objects.interfaces.ObjectId, text: str
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithFont
        ] = self._repo.get(object_id=obj_id)
        # TODO: think about incorrect obj type
        if obj:
            logging.debug('editing object old text=%s with new text=%s', obj.text, text)
            obj.text = text
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with text=%s', obj_id, text)

    def edit_color(
        self, obj_id: internal.objects.interfaces.ObjectId, color: str
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectCard,
            internal.objects.interfaces.IBoardObjectPen
        ] = self._repo.get(object_id=obj_id)
        # TODO: think about incorrect obj type
        if obj:
            logging.debug('editing object old color=%s with new color=%s', obj.color, color)
            obj.color = color
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with color=%s', obj_id, color)

    def edit_font(
        self, obj_id: internal.objects.interfaces.ObjectId, font: internal.models.Font
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithFont
        ] = self._repo.get(object_id=obj_id)
        # TODO: think about incorrect obj type
        if obj:
            logging.debug('editing object with old font=%s, to=%s', obj.font, font)
            obj.font = font
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with font=%s', obj_id, font)

    def move_object(
        self, obj_id: internal.objects.interfaces.ObjectId, delta: internal.models.Position
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithPosition
        ] = self._repo.get(object_id=obj_id)
        if not obj:
            logging.debug('no object id=%s found to edit with delta=%s', obj_id, delta)
            return
        logging.debug(
            'editing object with new delta=%s',
            delta
        )
        obj.position = obj.position + delta
        self._on_feature_finish()

    def edit_points(
        self, obj_id: internal.objects.interfaces.ObjectId,
        points: typing.List[internal.models.Position]
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectPen
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing object old points=%s with new points=%s',
                obj.points,
                points
            )
            obj.points = points
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with points=%s', obj_id, points)

    def edit_children_ids(
        self, obj_id: internal.objects.interfaces.ObjectId,
        children_ids: typing.Tuple[internal.objects.interfaces.ObjectId]
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectGroup
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing object old children_ids=%s with new children_ids=%s',
                obj.children_ids,
                children_ids
            )
            obj.children_ids = children_ids
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with children_ids=%s', obj_id, children_ids)

    def edit_width(
        self, obj_id: internal.objects.interfaces.ObjectId, width: float
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectPen
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing object old width=%s with new width=%s',
                obj.width,
                width
            )
            obj.width = width
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with width=%s', obj_id, width)

    def edit_connector_type(
        self, obj_id: internal.objects.interfaces.ObjectId, connector_type: str
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectConnector
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing object old connector_type=%s with new connector_type=%s',
                obj.connector_type,
                connector_type
            )
            obj.connector_type = connector_type
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with connector_type=%s', obj_id, connector_type)

    def edit_stroke_style(
        self, obj_id: internal.objects.interfaces.ObjectId, stroke_style: str
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectConnector
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing object old stroke_style=%s with new stroke_style=%s',
                obj.stroke_style,
                stroke_style
            )
            obj.stroke_style = stroke_style
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with stroke_style=%s', obj_id, stroke_style)
