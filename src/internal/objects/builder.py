from datetime import datetime

import internal.models
import internal.pub_sub.interfaces
from . import interfaces
from .impl.common import field_names
from .impl.object_id import generate_object_id
from .impl.type_impls import TYPE_IMPLS
from .types import BoardObjectType


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
        return TYPE_IMPLS[type](id, datetime.now().replace(microsecond=0), kwargs['position'], pub_sub_broker)
    if type == BoardObjectType.GROUP and 'children_ids' in kwargs:
        return TYPE_IMPLS[type](id, datetime.now().replace(microsecond=0), pub_sub_broker, kwargs['children_ids'])
    if type == BoardObjectType.CONNECTOR and 'start_id' in kwargs and 'end_id' in kwargs:
        return TYPE_IMPLS[type](id, datetime.now().replace(microsecond=0), pub_sub_broker, kwargs['start_id'], kwargs['end_id'])
    if type == BoardObjectType.PEN and 'points' in kwargs:
        return TYPE_IMPLS[type](id, datetime.now().replace(microsecond=0), pub_sub_broker, kwargs['points'])
    raise ValueError('No object to build')
