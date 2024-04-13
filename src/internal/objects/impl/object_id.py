import uuid

from internal.objects import interfaces


def generate_object_id() -> interfaces.ObjectId:
    return str(uuid.uuid4())
