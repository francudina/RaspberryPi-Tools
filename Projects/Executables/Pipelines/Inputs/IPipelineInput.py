import logging
from abc import ABC, abstractmethod
from typing import List, Dict

from Projects.AutonomousDriving.Config.Arguments import Arguments
from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
from Projects.Executables.Activities.ActivityType import ActivityType
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Pipelines.Inputs.InputConfig import InputConfig
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
from Projects.Executables.Utils import FileUtils


class IPipelineInput(ABC):

    def __init__(self, pipline_input_type: PipelineInputType):
        self.input_type: PipelineInputType = pipline_input_type

    @abstractmethod
    def _get_input(self, **kwargs) -> IActivity:
        pass

    def next_input(self, **kwargs) -> IActivity:
        return self._get_input(**kwargs)

    @staticmethod
    def get_pipeline_input(arguments: Arguments):
        from Projects.Executables.Pipelines.Inputs.Types.WebInput import WebInput
        from Projects.AutonomousDriving.Services.Algorithm.AlgorithmDrivingInputActivity import \
            AlgorithmDrivingInputActivity
        from Projects.Executables.Pipelines.Inputs.Types.ConsoleInput import ConsoleInput

        if arguments.pipeline_input == PipelineInputType.CONSOLE:
            return ConsoleInput(arguments)
        elif arguments.pipeline_input == PipelineInputType.WEB:
            return WebInput(arguments)
        elif arguments.pipeline_input == PipelineInputType.ALGORITHM:
            return AlgorithmDrivingInputActivity(arguments)
        else:
            raise ValueError(f"Wrong PipelineInputType sent: {arguments.pipeline_input}")

    def _get_init_configs(self, arguments: Arguments):
        device_config: {} = FileUtils.read_file(arguments.devices_config_file)

        # if commands were given, load them!
        file_data: Dict = {}
        if arguments.commands:
            file_data = FileUtils.read_file(arguments.commands, raise_exception=False)

        return device_config, file_data

    def _get_activity(self, device_config: {}, **file_data) -> IActivity:
        try:
            activity_type: str = file_data[InputConfig.ACTIVITY_TYPE_FIELD.value]

            if activity_type == ActivityType.DRIVING.value:
                commands: List[Dict] = file_data[InputConfig.DRIVING_COMMANDS.value]
                return DrivingActivity(device_config=device_config, commands=commands)
            else:
                return None

        except Exception as e:
            logging.error(f"Error during activity creation: {e}")
            return None
