import abc

import internal.models


class IUndoRedoManager(abc.ABC):
    @abc.abstractmethod
    def store_action(self, action: internal.models.IAction):
        pass

    @abc.abstractmethod
    def undo(self):
        pass

    @abc.abstractmethod
    def redo(self):
        pass
