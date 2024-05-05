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
                'editing object old focus=%s with new focus=%s ',
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
        self, obj_id: internal.objects.interfaces.ObjectId, **kwargs
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithFont
        ] = self._repo.get(object_id=obj_id)
        # TODO: think about incorrect obj type
        if obj:
            logging.debug('editing object with old font=%s, to=%s',
                          obj.font, kwargs)
            obj.update_font(**kwargs)
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with font=%s', obj_id, kwargs)

    def move_object(
            self, obj_id: internal.objects.interfaces.ObjectId, position: internal.models.Position
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithPosition
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing object old coord=%s with new coord=%s',
                obj.position,
                position
            )
            obj.position = position
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with position=%s', obj_id, position)

    def edit_points(
        self, obj_id: internal.objects.interfaces.ObjectId, points: typing.List[internal.models.Position]
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

    def change_table(
            self,
            obj_id: internal.objects.interfaces.ObjectId,
            list_col,
            list_row
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectTable
        ] = self._repo.get(object_id=obj_id)
        if obj:
            logging.debug(
                'editing shape of a table old shape: columns_width=%s and rows_height=%s, new shape: columns_width=%s '
                'and rows_height=%s ',
                obj.columns_width,
                obj.rows_height,
                list_col,
                list_row
            )
            obj.columns_width = list_col
            obj.rows_height = list_row
            obj.columns = len(list_col)
            obj.rows = len(list_row)
            self._on_feature_finish()
            return
        logging.debug('no object id=%s found to edit with column_width=%s and row_height=%s', obj_id, list_col,
                      list_row)

    def add_object_to(
            self,
            obj_id: internal.objects.interfaces.ObjectId,
            parent_obj_id: internal.objects.interfaces.ObjectId,
            coord: [int, int]
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithPosition
        ] = self._repo.get(object_id=obj_id)
        parent_obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectTable
        ] = self._repo.get(object_id=parent_obj_id)

        if not parent_obj:
            logging.debug('no table id=%s found', parent_obj)
        if not obj:
            logging.debug('no object id=%s found to add', obj_id)

        logging.debug('object added to a table: column=%s, row=%s', coord[0], coord[1])
        print('added to', coord)
        parent_obj.linked_objects[obj_id] = coord
        self._on_feature_finish()


    def remove_object_from(
            self,
            obj_id: internal.objects.interfaces.ObjectId,
            parent_obj_id: internal.objects.interfaces.ObjectId,
            coord: [int, int]
    ):
        obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectWithPosition
        ] = self._repo.get(object_id=obj_id)
        parent_obj: typing.Optional[
            internal.objects.interfaces.IBoardObjectTable
        ] = self._repo.get(object_id=parent_obj_id)

        if not parent_obj:
            logging.debug('no table id=%s found', parent_obj)
        if not obj:
            logging.debug('no object id=%s found to add', obj_id)

        logging.debug('object removed from a table: column=%s, row=%s', coord[0], coord[1])
        print('removed from', coord)
        del parent_obj.linked_objects[obj_id]
        self._on_feature_finish()
