import logging

from internal.controller import interfaces
import internal.models
import internal.repositories
import internal.storages


class Controller(interfaces.IController):
    def __init__(
        self,
        repo: internal.repositories.interfaces.IRepository,
        storage: internal.storages.interfaces.IStorage,
        pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ):
        self._repo = repo
        self._storage = storage
        self._pub_sub_broker = pub_sub_broker

    # TODO: feature abstaction
    def _on_feature_finish(self):
        logging.debug('start executing feature finish pipeline')
        # 1) Process pub-sub
        # 2) Extract updates from repo
        # 3) Push updates to storage
        # 4) Push updates to UndoRedoManager (future work)
        # Fetch updates from storage and update repo sometimes (future work)

        logging.debug('processing published pub_sub events')
        self._pub_sub_broker.process_published(self._repo)

        logging.debug('saving updates to the storage')
        # TODO: myb better API for updates?
        updates = self._repo.get_updated()
        raw_updates: internal.storages.interfaces.IStorage.UpdatesType = dict()
        for (obj_id, update) in updates.items():
            raw_updates[str(obj_id)] = update
        self._storage.update(raw_updates)
        logging.debug('finished exectuing feature finish pipeline')

    def create_object(
        self, type: internal.objects.BoardObjectType, position: internal.models.Position
    ):
        logging.debug('creating object with type=%s, position=%s', type, position)
        obj = internal.objects.build_by_type(type, position, self._pub_sub_broker)
        self._repo.add(obj)
        self._on_feature_finish()
