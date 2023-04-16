from typing import Dict

from Projects.AutonomousDriving.Config.Arguments import Arguments
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Pipelines.Inputs.IPipelineInput import IPipelineInput
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
from Projects.Executables.Utils import FileUtils


class ConsoleInput(IPipelineInput):

    def __init__(self, arguments: Arguments):
        super(ConsoleInput, self).__init__(PipelineInputType.CONSOLE)
        self.arguments: Arguments = arguments
        # config and init commands
        device_config, file_data = self._get_init_configs(self.arguments)
        self.device_config: Dict = device_config
        self.file_data: Dict = file_data

    def _get_input(self, **kwargs) -> IActivity:
        iter_num: int = 3

        activity: IActivity = None
        while iter_num > 1:
            iter_num -= 1

            # if commands were not given
            if not self.file_data:
                input_data: str = self._read_input(iter_num)
                self.file_data: Dict = FileUtils.read_file(input_data)

            if self.file_data is None:
                continue

            activity = self._get_activity(device_config=self.device_config, **self.file_data)
            # reset loaded data after activity creation!
            self.file_data = {}

            if activity is None:
                continue
            break

        return activity

    def _read_input(self, iter_num: int) -> str:
        return input(f'\n## Insert ACTIVITY Config file path (attempts remaining: {iter_num}): ')
