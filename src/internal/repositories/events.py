import internal.pub_sub.interfaces
import internal.objects.interfaces

EVENT_TYPE_OBJECT_ADDED = 'repo_object_added'
EVENT_TYPE_OBJECT_DELETED = 'repo_object_deleted'


class EventObjectAdded(internal.pub_sub.interfaces.Event):
    def __init__(self, object_id: internal.objects.interfaces.ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_ADDED)
        self._object_id = object_id

    @property
    def object_id(self) -> internal.objects.interfaces.ObjectId:
        return self._object_id


class EventObjectDeleted(internal.pub_sub.interfaces.Event):
    def __init__(self, object_id: internal.objects.interfaces.ObjectId):
        super().__init__(EVENT_TYPE_OBJECT_DELETED)
        self._object_id = object_id

    @property
    def object_id(self) -> internal.objects.interfaces.ObjectId:
        return self._object_id
