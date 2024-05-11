from typing import Optional

from .. import interfaces

import internal.models


class UndoRedoManager(interfaces.IUndoRedoManager):
    _history: list[internal.models.IAction]
    _max_history_size: int
    _cur_pos: int   # position of last applied action in _history

    def __init__(self, max_history_size: int):
        if max_history_size < 1:
            raise ValueError('max_history_size < 1')

        self._history = []
        self._max_history_size = max_history_size
        self._cur_pos = -1

    def store_action(self, action: internal.models.IAction):
        if self._cur_pos != len(self._history) - 1:
            del self._history[self._cur_pos + 1]
        self._history.append(action)

        self._history = self._history[: self._max_history_size]
        self._cur_pos = len(self._history) - 1

    def undo(self):
        if self._cur_pos == -1:
            return
        self._history[self._cur_pos].undo()
        self._cur_pos -= 1

    def redo(self):
        if self._cur_pos == len(self._history) - 1:
            return
        self._history[self._cur_pos + 1].do()
        self._cur_pos += 1
