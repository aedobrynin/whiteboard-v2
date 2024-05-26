import os
import logging

import internal.objects.interfaces
import internal.objects.events
import internal.repositories.events
import internal.repositories.interfaces
import internal.view.dependencies
import internal.view.objects.interfaces
import internal.view.utils
from internal.view.objects.impl.object import ViewObject

_DEFAULT_WIDTH = 2
_DEFAULT_COLOR = 'gray'

_TRANSPARENT_FILE_PATH = os.path.join(os.path.dirname(__file__), 'xbms/transparent.xbm')


class GroupObject(ViewObject):
    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectGroup,
    ):
        ViewObject.__init__(self, obj)
        self._children_ids = obj.children_ids
        invisible_rect = self._get_invisible_rect(dependencies)
        self._rectangle_id = dependencies.canvas.create_rectangle(
            *invisible_rect.as_tkinter_rect(),
            outline='green',  # for tests
            fill=_DEFAULT_COLOR,  # do not remove
            stipple=f'@{_TRANSPARENT_FILE_PATH}',
            width=_DEFAULT_WIDTH,
            tags=[obj.id],
        )
        for child_id in obj.children_ids:
            dependencies.canvas.tag_lower(obj.id, child_id)
            dependencies.canvas.addtag_withtag(obj.id, child_id)

        self._subscribe_to_repo_object_events(dependencies)

    @property
    def rectangle_id(self):
        return self._rectangle_id

    def widgets(self, dependencies: internal.view.dependencies.Dependencies):
        return []

    def destroy(self, dependencies: internal.view.dependencies.Dependencies):
        for child_id in self._children_ids:
            dependencies.pub_sub_broker.unsubscribe(self.id, child_id)
            dependencies.canvas.dtag(child_id, self.id)
        dependencies.pub_sub_broker.unsubscribe(self.id, self.id)
        dependencies.canvas.delete(self.id)

    def _get_invisible_rect(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> internal.view.utils.geometry.Rectangle:
        invisible_rect = None
        for child_id in self._children_ids:
            child_obj = dependencies.objects_storage.get_opt_by_id(child_id)
            if not child_obj:
                logging.warning('child already removed')
                continue
            child_rect = child_obj.get_border_rectangle(dependencies)
            invisible_rect = internal.view.utils.geometry.get_min_containing_rect(
                invisible_rect, child_rect
            )
        assert invisible_rect is not None
        return invisible_rect

    def _subscribe_to_repo_object_events(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.subscribe(
            self.id,
            internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
            internal.repositories.events.EVENT_TYPE_OBJECT_DELETED,
            lambda publisher, event, repo: (
                self._get_removal_children_ids_from_repo(dependencies, event)
            ),
        )
        dependencies.pub_sub_broker.subscribe(
            self.id,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_CHILDREN_IDS,
            lambda publisher, event, repo: (
                self._get_update_children_ids_from_repo(dependencies, event)
            ),
        )
        for child_id in self._children_ids:
            dependencies.pub_sub_broker.subscribe(
                self.id,
                child_id,
                internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_SIZE,
                lambda publisher, event, repo: self._get_update_children_from_repo(dependencies),
            )
            dependencies.pub_sub_broker.subscribe(
                self.id,
                child_id,
                internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
                lambda publisher, event, repo: self._get_update_children_from_repo(dependencies),
            )

    def _get_removal_children_ids_from_repo(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        event: internal.repositories.events.EventObjectDeleted,
    ):
        if event.object_id not in self._children_ids or not dependencies.repo.get(self.id):
            return
        children_ids = [child_id for child_id in self._children_ids if child_id != event.object_id]
        if len(children_ids) <= 1:
            dependencies.controller.delete_object(self.id)
            return
        dependencies.pub_sub_broker.unsubscribe(self.id, event.object_id)
        dependencies.controller.edit_children_ids(self.id, children_ids)

    def _get_update_children_ids_from_repo(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        event: internal.repositories.events.EventObjectDeleted,
    ):
        obj: internal.objects.interfaces.IBoardObjectGroup = dependencies.repo.get(event.object_id)
        if not obj:
            logging.warning('object not found')
        for child_id in self._children_ids:
            dependencies.canvas.dtag(child_id, self.id)
        self._children_ids = obj.children_ids
        for child_id in self._children_ids:
            dependencies.canvas.addtag_withtag(obj.id, child_id)
        self._get_update_children_from_repo(dependencies)

    def _get_update_children_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        invisible_rect = self._get_invisible_rect(dependencies)
        dependencies.canvas.coords(self.rectangle_id, *invisible_rect.as_tkinter_rect())
