from typing import Optional, List

import internal.objects.interfaces

from .. import interfaces


class MockRepository(interfaces.IRepository):
    def __init__(self):
        pass

    def get(
        self, object_id: internal.objects.interfaces.ObjectId
    ) -> Optional[internal.objects.interfaces.IBoardObject]:
        raise NotImplementedError()

    def get_all(self) -> List[internal.objects.interfaces.IBoardObject]:
        raise NotImplementedError()

    def get_all(
        self
    ) -> List[internal.objects.interfaces.IBoardObject]:
        # TODO: implement when needed
        pass

    def add(self, object: internal.objects.interfaces.IBoardObject) -> None:
        raise NotImplementedError()

    def delete(self, object_id: internal.objects.interfaces.ObjectId) -> None:
        raise NotImplementedError()

    def get_updated(self) -> dict[internal.objects.interfaces.ObjectId, Optional[dict]]:
        raise NotImplementedError()
