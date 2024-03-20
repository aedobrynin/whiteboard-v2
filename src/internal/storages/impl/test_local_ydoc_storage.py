from .local_ydoc_storage import LocalYDocStorage


def test_local_ydoc_storage_save_empty(tmp_path):
    path = tmp_path / 'storage'
    storage = LocalYDocStorage(path)
    storage.save()

    storage = LocalYDocStorage(path)
    assert len(storage.get_serialized_objects()) == 0


def test_local_ydoc_storage_save(tmp_path):
    path = tmp_path / 'storage'
    storage = LocalYDocStorage(path)

    key = 'obj_id'
    value = {'a': 'b'}
    storage.update({key: value})
    storage.save()

    storage = LocalYDocStorage(path)
    assert storage.get_serialized_objects() == {key: value}
