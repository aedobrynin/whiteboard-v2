from .ydoc_storage import YDocStorage


def test_ydoc_storage_insertion():
    storage = YDocStorage()
    key = 'obj_id'
    storage.update({key: {'a': 'b'}})
    assert storage.get_serialized_objects() == {key: {'a': 'b'}}


def test_ydoc_storage_update():
    storage = YDocStorage()

    key = 'obj_id'
    initial_value = {'a': 'b'}
    storage.update({key: initial_value})
    assert storage.get_serialized_objects() == {key: initial_value}

    updated_value = {'a': 'c', 'd': 'e'}
    storage.update({key: updated_value})
    assert storage.get_serialized_objects() == {key: updated_value}


def test_ydoc_storage_delete():
    storage = YDocStorage()
    key = 'obj_id'

    initial_value = {'a': 'b'}
    storage.update({key: initial_value})
    assert storage.get_serialized_objects() == {key: initial_value}
    storage.update({key: None})
    assert len(storage.get_serialized_objects()) == 0
