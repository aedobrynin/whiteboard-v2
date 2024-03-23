from internal.controller import interfaces
import internal.models
import internal.repositories
import internal.storages


class Controller(interfaces.IController):
    def __init__(
        self,
        repo: internal.repositories.interfaces.IRepository,
        storage: internal.storages.interfaces.IStorage,
    ):
        self._repo = repo
        self._storage = storage

    def create_object(
        self, type: internal.objects.BoardObjectType, position: internal.models.Position
    ):
        # 1) Create Object
        # 2) Add it to repo
        # 3) Process pub-sub (future work)
        # 4) Extract updates from repo
        # 5) Push updates to storage
        # Fetch updates from storage and update repo sometimes (future work)

        obj = internal.objects.build_by_type(type, position)
        self._repo.add(obj)
        # Process pub-sub here (3)

        # TODO: myb better API for updates?
        updates = self._repo.get_updated()
        raw_updates: internal.storages.interfaces.IStorage.UpdatesType = dict()
        for (obj_id, update) in updates.items():
            raw_updates[str(obj_id)] = update
        self._storage.update(raw_updates)
