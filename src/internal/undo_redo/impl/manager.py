import logging

import internal.models
from .. import interfaces


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
        logging.debug('storing action in undo-redo manager')   # TODO: log action name
        if self._cur_pos != len(self._history) - 1:
            del self._history[self._cur_pos + 1]
        self._history.append(action)

        self._history = self._history[-self._max_history_size :]
        self._cur_pos = len(self._history) - 1

    def undo(self):
        logging.debug('trying to undo')
        if self._cur_pos == -1:
            logging.debug('nothing to undo')
            return
        self._history[self._cur_pos].undo()
        logging.debug('successfully undid action')
        self._cur_pos -= 1

    def redo(self):
        logging.debug('trying to redo')
        if self._cur_pos == len(self._history) - 1:
            logging.debug('nothing to redo')
            return
        self._history[self._cur_pos + 1].do()
        logging.debug('successfully redid action')
        self._cur_pos += 1
