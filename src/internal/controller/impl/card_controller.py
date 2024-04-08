import logging

import internal.models
import internal.objects
import internal.objects.interfaces
import internal.pub_sub.interfaces
import internal.repositories.interfaces
import internal.storages
from . import Controller
from .. import interfaces


class CardController(interfaces.ICardController, Controller):

    def __init__(
            self,
            repo: internal.repositories.interfaces.IRepository,
            storage: internal.storages.interfaces.IStorage,
            pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    ):
        Controller.__init__(self, repo, storage, pub_sub_broker)

    def edit_text(
            self,
            obj_id: internal.objects.interfaces.ObjectId,
            text: str
    ):
        obj: internal.objects.interfaces.IBoardObjectCard = self._repo.get(object_id=obj_id)
        logging.debug('editing text of object old text=%s, new text=%s ', obj.text, text)
        obj.text = text
        self._on_feature_finish()
