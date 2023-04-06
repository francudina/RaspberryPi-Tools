from abc import ABC, abstractmethod
from typing import Dict

from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


class IPipelineInput(ABC):

    def __init__(self, input_type:  PipelineInputType):
        self.input_type = input_type

    @abstractmethod
    def _get_input(self, **kwargs) -> IActivity:
        pass

    def next_input(self, **kwargs) -> IActivity:
        return self._get_input(**kwargs)
        # iter_num: int = 3
        # chosen_activity: IActivity = None
        # while iter_num > 0:
        #     iter_num -= 1
        #     chosen_activity = self._get_input(**kwargs)
        #     if chosen_activity is not None:
        #         break
        # return chosen_activity

    @staticmethod
    def get_pipeline_input(pipeline_input_type: PipelineInputType):
        from Projects.Executables.Pipelines.Inputs.Types.WebInput import WebInput
        from Projects.Executables.Pipelines.Inputs.Types.AlgorithmInput import AlgorithmInput
        from Projects.Executables.Pipelines.Inputs.Types.ConsoleInput import ConsoleInput

        if pipeline_input_type == PipelineInputType.CONSOLE:
            return ConsoleInput()
        elif pipeline_input_type == PipelineInputType.WEB:
            return WebInput()
        elif pipeline_input_type == PipelineInputType.ALGORITHM:
            return AlgorithmInput()
        else:
            raise ValueError(f"Wrong PipelineInputType sent: {pipeline_input_type}")
