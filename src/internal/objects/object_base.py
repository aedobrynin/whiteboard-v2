from typing import Any, List
from dataclasses import dataclass
import uuid

from internal.fields.serializable_field_base import SerializableFieldBase
from internal.fields import UuidField


@dataclass(frozen=True)
class FieldUpdateInfo:
    field_name: str
    initial_value: Any
    current_value: Any


class ObjectBase:
    _fields: dict[str, SerializableFieldBase]

    # TODO: forbid id update
    id: uuid.UUID

    def __init__(self, id: uuid.UUID):
        self.__dict__['_fields'] = {}
        self._add_field('id', UuidField(id))

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self._fields:
            self._fields[__name].value = __value
        else:
            self.__dict__[__name] = __value

    def __getattr__(self, __name: str) -> Any:
        if __name in self._fields:
            return self._fields[__name].value
        return self.__dict__[__name]

    # Should be called only from derived classes
    def _add_field(self, name: str, field: SerializableFieldBase):
        self._fields[name] = field

    def get_changed_fields(self) -> List[FieldUpdateInfo]:
        res = []
        for name, field in self._fields.items():
            if field.is_changed():
                res.append(
                    FieldUpdateInfo(
                        field_name=name,
                        initial_value=field.get_initial_value(),
                        current_value=field.value,
                    )
                )
        return res
