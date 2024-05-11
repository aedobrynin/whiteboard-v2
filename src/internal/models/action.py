import abc


class IAction(abc.ABC):
    # TODO: deps
    @abc.abstractmethod
    def do(self):
        pass

    # TODO: deps
    @abc.abstractmethod
    def undo(self):
        pass
