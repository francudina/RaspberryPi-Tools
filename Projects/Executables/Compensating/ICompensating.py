from abc import abstractmethod

from Projects.Executables.IExecutable import IExecutable


class ICompensating(IExecutable):

    def __init__(self):
        super(ICompensating, self).__init__()

    @abstractmethod
    def compensate(self, **kwargs) -> bool:
        pass
