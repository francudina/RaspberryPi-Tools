from abc import ABC, abstractmethod

from Projects.Executables.Commands.ICommand import ICommand
from Projects.Executables.IExecutable import IExecutable
from Projects.Queues.IQueue import IQueue


class IAlgorithm(IQueue[ICommand], IExecutable, ABC):
    """
    Algorithm interface.
    """

    @abstractmethod
    def pause(self) -> bool:
        pass

    @abstractmethod
    def resume(self) -> bool:
        pass
