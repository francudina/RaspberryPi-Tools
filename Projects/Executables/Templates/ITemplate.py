from abc import abstractmethod

from Projects.Executables.IExecutable import IExecutable
from Projects.Executables.Pipelines.IPipeline import IPipeline


class ITemplate(IExecutable):

    @property
    @abstractmethod
    def pipeline(self) -> IPipeline:
        pass
