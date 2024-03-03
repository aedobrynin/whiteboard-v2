import abc
from typing import Any, Callable, Optional


class SerializableFieldBase:
    _initial_val: Any
    _val: Any
    _after_value_change: Optional[Callable[[], None]]

    def __init__(self, val, after_value_change: Optional[Callable[[], None]] = None):
        self._initial_val = val
        self._val = val
        self._after_value_change = after_value_change

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, new_val):
        self._val = new_val
        if self._after_value_change is not None:
            self._after_value_change()

    @abc.abstractmethod
    def serialize(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def from_serialized():
        pass

    def is_changed(self) -> bool:
        return self._initial_val != self._val

    def get_initial_value(self) -> Any:
        return self._initial_val
