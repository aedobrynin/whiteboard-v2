from .local_ydoc_storage import LocalYDocStorage


def test_insertion():
    storage = LocalYDocStorage()
    key = 'obj_id'
    storage.update({key: {'a': 'b'}})
    assert storage.get_serialized_objects() == {key: {'a': 'b'}}


def test_update():
    storage = LocalYDocStorage()
    key = 'obj_id'

    initial_repr = {'a': 'b'}
    storage.update({key: initial_repr})
    assert storage.get_serialized_objects() == {key: initial_repr}

    updated_repr = {'a': 'c', 'd': 'e'}
    storage.update({key: updated_repr})
    assert storage.get_serialized_objects() == {key: updated_repr}


def test_delete():
    storage = LocalYDocStorage()
    key = 'obj_id'

    initial_repr = {'a': 'b'}
    storage.update({key: initial_repr})
    assert storage.get_serialized_objects() == {key: initial_repr}
    storage.update({key: None})
    assert len(storage.get_serialized_objects()) == 0
