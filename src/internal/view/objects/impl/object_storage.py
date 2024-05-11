from __future__ import annotations

import logging
from typing import Type, Optional

import internal.objects.interfaces
import internal.pub_sub.interfaces
import internal.repositories.events
import internal.repositories.interfaces
import internal.view.dependencies
from ..interfaces import IViewObject, IViewObjectStorage
from ...consts import VIEW_OBJECT_ID


class ViewObjectStorage(IViewObjectStorage):
    _objects: dict[str, IViewObject]
    _object_types: dict[internal.objects.BoardObjectType, Type[IViewObject]]

    def __init__(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        self._objects = {}
        self._object_types = {}
        self._subscribe_to_create_object_event(dependencies)
        self._subscribe_to_delete_object_event(dependencies)

    def create_view_objects(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> None:
        for obj in dependencies.repo.get_all():
            self._create_obj(obj.id, dependencies)

    def _subscribe_to_create_object_event(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
            internal.repositories.events.EVENT_TYPE_OBJECT_ADDED,
            lambda publisher, event, repo: self._create_obj(event.object_id, dependencies)
        )

    def _subscribe_to_delete_object_event(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
            internal.repositories.events.EVENT_TYPE_OBJECT_DELETED,
            lambda publisher, event, repo: self._delete_obj(event.object_id, dependencies)
        )

    def _create_obj(
        self,
        obj_id: internal.objects.interfaces.ObjectId,
        dependencies: internal.view.dependencies.Dependencies
    ):
        obj: internal.objects.interfaces.IBoardObject = dependencies.repo.get(obj_id)
        if obj.id in self._objects:
            logging.debug('obj_id(%s) already in canvas', obj.id)
        if obj.type in self._object_types:
            self._objects[obj_id] = self._object_types[obj.type](dependencies, obj)  # type: ignore
        else:
            logging.debug('type(%s) of object not found in view', obj.type)

    def _delete_obj(
        self,
        obj_id: internal.objects.interfaces.ObjectId,
        dependencies: internal.view.dependencies.Dependencies
    ):
        if obj_id in self._objects:
            obj = self._objects.pop(obj_id)
            obj.destroy(dependencies)
            logging.debug('deleting the object=%s from canvas', obj_id)
        else:
            logging.debug('object=%s already deleted from canvas', obj_id)

    def register_object_type(
        self, type_name: internal.objects.BoardObjectType, type_class: Type[IViewObject]
    ):
        self._object_types[type_name] = type_class

    def get_by_id(
        self, object_id: str
    ) -> IViewObject:
        return self._objects[object_id]

    def get_opt_by_id(
        self, object_id: str
    ) -> Optional[IViewObject]:
        return self._objects.get(object_id)

    def get_current(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> IViewObject:
        tags = dependencies.canvas.gettags('current')
        if not tags:
            raise KeyError('No tags for current object')
        return self.get_by_id(tags[0])

    def get_current_opt(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> Optional[IViewObject]:
        tags = dependencies.canvas.gettags('current')
        if not tags:
            logging.debug('No tags for current object')
            return None
        return self.get_opt_by_id(tags[0])
