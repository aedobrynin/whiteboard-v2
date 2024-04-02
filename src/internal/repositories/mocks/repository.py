from typing import Optional

import internal.objects.interfaces

from .. import interfaces


class MockRepository(interfaces.IRepository):
    def __init__(self):
        pass

    def get(
        self, object_id: internal.objects.interfaces.ObjectId
    ) -> Optional[internal.objects.interfaces.IBoardObject]:
        # TODO: implement when needed
        return None

    def add(self, object: internal.objects.interfaces.IBoardObject) -> None:
        # TODO: implement when needed
        pass

    def delete(self, object_id: internal.objects.interfaces.ObjectId) -> None:
        # TODO: implement when needed
        pass

    def get_updated(self) -> dict[internal.objects.interfaces.ObjectId, Optional[dict]]:
        # TODO: implement when needed
        return {}
