import uuid

from .impl.type_impls import TYPE_IMPLS
from .impl.common import field_names
from . import interfaces
from .types import BoardObjectType
import internal.models
import internal.pub_sub.interfaces


def build_from_serialized(
    data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
) -> interfaces.IBoardObject:
    return TYPE_IMPLS[BoardObjectType(data[field_names.TYPE_FIELD])].from_serialized(
        data, pub_sub_broker
    )


# TODO: move to impl
def _generate_id() -> interfaces.ObjectId:
    return uuid.uuid4()


# TODO: better API for building
def build_by_type(
    type: BoardObjectType,
    position: internal.models.Position,
    pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
) -> interfaces.IBoardObjectWithPosition:
    id = _generate_id()
    return TYPE_IMPLS[type](id, position, pub_sub_broker)
