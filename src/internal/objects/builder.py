import internal.models
import internal.pub_sub.interfaces

from .impl.type_impls import TYPE_IMPLS
from .impl.common import field_names
from . import interfaces
from .types import BoardObjectType
from .impl.object_id import generate_object_id


def build_from_serialized(
    data: dict, pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
) -> interfaces.IBoardObject:
    return TYPE_IMPLS[BoardObjectType(data[field_names.TYPE_FIELD])].from_serialized(
        data, pub_sub_broker
    )


# TODO: better API for building
# TODO: it might be a little inconsistent when we add another pub_sub_broker,
#       because it will be possible that repository and object will have different brokers.
#       myb we want to restrict that
def build_by_type(
    type: BoardObjectType,
    pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker,
    **kwargs
) -> interfaces.IBoardObjectWithPosition:
    id = generate_object_id()
    if 'position' in kwargs and isinstance(kwargs['position'], internal.models.Position):
        return TYPE_IMPLS[type](id, kwargs['position'], pub_sub_broker)
    if type == BoardObjectType.GROUP and 'children_ids' in kwargs:
        return TYPE_IMPLS[type](id, pub_sub_broker, kwargs['children_ids'])
    if type == BoardObjectType.PEN and 'points' in kwargs:
        return TYPE_IMPLS[type](id, pub_sub_broker, kwargs['points'])
    raise ValueError('No object to build')
