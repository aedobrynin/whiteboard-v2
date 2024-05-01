from .interfaces import ObjectId

import internal.pub_sub.event

EVENT_TYPE_OBJECT_MOVED = 'object_moved'
EVENT_TYPE_OBJECT_CHANGED_SIZE = 'object_changed_size'


class EventObjectMoved(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_MOVED)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedSize(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_SIZE)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id
