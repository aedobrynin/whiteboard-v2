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

    # TODO: feature abstaction
    def _on_feature_finish(self):
        # 1) Process pub-sub (future work)
        # 2) Extract updates from repo
        # 3) Push updates to storage
        # 4) Push updates to UndoRedoManager (future work)
        # Fetch updates from storage and update repo sometimes (future work)

        # TODO: Process pub-sub here (1)
        # TODO: myb better API for updates?
        updates = self._repo.get_updated()
        raw_updates: internal.storages.interfaces.IStorage.UpdatesType = dict()
        for (obj_id, update) in updates.items():
            raw_updates[str(obj_id)] = update
        self._storage.update(raw_updates)

    def create_object(
        self, type: internal.objects.BoardObjectType, position: internal.models.Position
    ):
        obj = internal.objects.build_by_type(type, position)
        self._repo.add(obj)
        self._on_feature_finish()
