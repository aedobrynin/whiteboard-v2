from .interfaces import ObjectId

import internal.pub_sub.event

EVENT_TYPE_OBJECT_MOVED = 'object_moved'
EVENT_TYPE_OBJECT_CHANGED_SIZE = 'object_changed_size'
EVENT_TYPE_OBJECT_CHANGED_FONT = 'object_changed_font'
EVENT_TYPE_OBJECT_CHANGED_TEXT = 'object_changed_text'
EVENT_TYPE_OBJECT_CHANGED_COLOR = 'object_changed_color'


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


class EventObjectChangedFont(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_FONT)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedText(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_TEXT)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedColor(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_COLOR)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id
