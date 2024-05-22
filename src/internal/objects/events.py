import internal.pub_sub.event
from .interfaces import ObjectId

EVENT_TYPE_OBJECT_MOVED = 'object_moved'
EVENT_TYPE_OBJECT_CHANGED_SIZE = 'object_changed_size'
EVENT_TYPE_OBJECT_CHANGED_FONT = 'object_changed_font'
EVENT_TYPE_OBJECT_CHANGED_TEXT = 'object_changed_text'
EVENT_TYPE_OBJECT_CHANGED_COLOR = 'object_changed_color'
EVENT_TYPE_OBJECT_CHANGED_WIDTH = 'object_changed_width'
EVENT_TYPE_OBJECT_CHANGED_CONNECTOR_TYPE = 'object_changed_connector_type'
EVENT_TYPE_OBJECT_CHANGED_STROKE_STYLE = 'object_changed_stroke_style'
EVENT_TYPE_OBJECT_CHANGED_POINTS = 'object_changed_points'
EVENT_TYPE_OBJECT_CHANGED_CHILDREN_IDS = 'object_changed_children_ids'
EVENT_TYPE_OBJECT_CHANGED_LEXER = 'object_changed_lexer'


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


class EventObjectChangedWidth(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_WIDTH)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedConnectorType(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_CONNECTOR_TYPE)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedStrokeStyle(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_STROKE_STYLE)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedPoints(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_POINTS)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedChildrenIds(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_CHILDREN_IDS)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id


class EventObjectChangedLexer(internal.pub_sub.event.Event):
    def __init__(self, object_id: ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_CHANGED_LEXER)
        self._object_id = object_id

    @property
    def object_id(self) -> ObjectId:
        return self._object_id
