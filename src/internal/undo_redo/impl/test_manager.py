from . import UndoRedoManager

import internal.models


class AppendAction(internal.models.IAction):
    def __init__(self, lst, val):
        self._lst = lst
        self._val = val

    def do(self):
        self._lst.append(self._val)

    def undo(self):
        self._lst.pop()


def test_undo_redo_manager_undo():
    manager = UndoRedoManager(5)

    lst = []
    val = 1
    act = AppendAction(lst, val)
    act.do()
    assert lst == [1]
    manager.store_action(act)

    manager.undo()
    assert len(lst) == 0
    manager.undo()  # should be no-op
    assert len(lst) == 0


def test_undo_redo_manager_redo():
    manager = UndoRedoManager(5)

    lst = []
    val = 1
    act = AppendAction(lst, val)
    act.do()
    assert lst == [1]
    manager.store_action(act)

    manager.undo()
    assert len(lst) == 0
    manager.redo()
    assert lst == [val]
    manager.redo()   # should be no-op
    assert lst == [val]


def test_undo_redo_manager_history_size():
    history_size = 5
    manager = UndoRedoManager(history_size)

    lst = []

    for i in range(history_size + 1):
        act = AppendAction(lst, i)
        act.do()
        manager.store_action(act)
    assert lst == list(range(history_size + 1))

    for i in range(history_size + 1):
        manager.undo()
    assert lst == [0]


def test_undo_redo_manager_complicated_undo_redo_series():
    history_size = 5
    manager = UndoRedoManager(history_size)

    lst = []
    for i in range(3):
        act = AppendAction(lst, i)
        act.do()
        manager.store_action(act)
    assert lst == [0, 1, 2]
    manager.undo()
    assert lst == [0, 1]
    manager.undo()
    assert lst == [0]
    manager.redo()
    assert lst == [0, 1]
    manager.undo()
    assert lst == [0]
    manager.redo()
    assert lst == [0, 1]
    manager.redo()
    assert lst == [0, 1, 2]
    manager.undo()
    assert lst == [0, 1]
    manager.undo()
    assert lst == [0]
    manager.undo()
    assert lst == []
    manager.undo()   # should be no-op
    assert lst == []
    manager.redo()
    assert lst == [0]
    manager.redo()
    assert lst == [0, 1]
    manager.redo()
    assert lst == [0, 1, 2]
    manager.redo()   # should be no-op
    assert lst == [0, 1, 2]


def test_undo_redo_manager_tail_is_removed_on_store():
    history_size = 5
    manager = UndoRedoManager(history_size)

    lst = []
    for i in range(3):
        act = AppendAction(lst, i)
        act.do()
        manager.store_action(act)
    assert lst == [0, 1, 2]

    manager.undo()
    manager.undo()
    assert lst == [0]
    act = AppendAction(lst, 3)
    act.do()
    manager.store_action(act)
    assert lst == [0, 3]
    manager.redo()  # should be no-op
    assert lst == [0, 3]
