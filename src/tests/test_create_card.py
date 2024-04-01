import internal


def test_create_object(tmp_path):
    type_ = internal.objects.BoardObjectType.card
    position = internal.models.Position(1, 2, 3)

    # TODO: is this bad that we access 'impl' directly?
    storage = internal.storages.impl.LocalYDocStorage(tmp_path / 'storage')
    repo = internal.repositories.impl.Repository([])
    broker = internal.pub_sub.impl.PubSubBroker()

    controller = internal.controller.impl.Controller(repo, storage, broker)
    controller.create_object(
        type_,
        position,
    )

    assert len(repo.get_updated()) == 0
    serialized_objects = storage.get_serialized_objects()
    assert len(serialized_objects) == 1

    serialized_obj = list(serialized_objects.values())[0]
    obj: internal.objects.interfaces.IBoardObjectCard = internal.objects.build_from_serialized(
        serialized_obj, broker
    )   # type: ignore
    assert isinstance(obj, internal.objects.interfaces.IBoardObjectCard)
    assert obj.type == type_
    assert obj.position == position
    # TODO: default text as const
    assert obj.text == 'text'

    # TODO: test broker events
