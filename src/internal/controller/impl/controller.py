from internal.controller import interfaces
import internal.models


class Controller(interfaces.IController):
    def __init__(self):
        pass

    def create_object(
        self, position: internal.models.Position, type: internal.objects.BoardObjectType
    ):
        # 1) Create Object
        # 2) Add it to repo
        # 3) Process pub-sub (future work)
        # 4) Extract updates from repo
        # 5) Push updates to storage
        # Fetch updates from storage and update repo sometimes (future work)
        pass
