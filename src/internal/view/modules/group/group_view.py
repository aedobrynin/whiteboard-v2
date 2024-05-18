from __future__ import annotations

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


class GroupObject(ViewObject):
    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectGroup
    ):
        ViewObject.__init__(self, obj)
        self._children_ids = obj.children_ids
        invisible_rect = self._get_invisible_rect(dependencies)
        self._rectangle_id = dependencies.canvas.create_rectangle(
            *invisible_rect.as_tkinter_rect(),
            outline='green',  # for tests
            fill=_DEFAULT_COLOR,  # do not remove
            stipple='@internal/view/modules/group/xbms/transparent.xbm',
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

    @property
    def children_ids(self):
        return self._children_ids

    def _get_invisible_rect(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> internal.view.utils.geometry.Rectangle:
        invisible_rect = None
        for child_id in self.children_ids:
            child_obj = dependencies.objects_storage.get_opt_by_id(child_id)
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
            self.id, internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
            internal.repositories.events.EVENT_TYPE_OBJECT_DELETED,
            lambda publisher, event, repo: self._get_update_children_ids_from_repo(dependencies,
                                                                                   event)
        )
        for child_id in self.children_ids:
            dependencies.pub_sub_broker.subscribe(
                self.id, child_id,
                internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_SIZE,
                lambda publisher, event, repo: self._get_update_children_from_repo(dependencies),
            )
            dependencies.pub_sub_broker.subscribe(
                self.id, child_id,
                internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
                lambda publisher, event, repo: self._get_update_children_from_repo(dependencies),
            )

    def _get_update_children_ids_from_repo(
        self, dependencies: internal.view.dependencies.Dependencies,
        event: internal.repositories.events.EventObjectDeleted
    ):
        if event.object_id not in self._children_ids or not dependencies.repo(self.id):
            return
        dependencies.canvas.dtag(event.object_id, self.id)
        dependencies.pub_sub_broker.unsubscribe(self.id, event.object_id)
        self._children_ids.remove(event.object_id)
        if len(self._children_ids) <= 1:
            dependencies.controller.delete_object(self.id)

    def _get_update_children_from_repo(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        invisible_rect = self._get_invisible_rect(dependencies)
        dependencies.canvas.coords(self.rectangle_id, *invisible_rect.as_tkinter_rect())
