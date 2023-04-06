from abc import ABC, abstractmethod
from typing import List, Dict

from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.LogData import LogData


class IExecutable(ABC):

    def __init__(self):
        # init
        self.status: ExecutablesStatus = ExecutablesStatus.NOT_STARTED
        self.state: Dict = dict()
        self.log: List[LogData] = list[LogData]()

    @abstractmethod
    def start(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def stop(self, **kwargs) -> bool:
        pass
