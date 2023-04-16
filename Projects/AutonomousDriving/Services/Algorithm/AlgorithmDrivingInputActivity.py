import logging
from typing import List, Dict

from Projects.AutonomousDriving.Config.Arguments import Arguments
from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
from Projects.Executables.Activities.ActivityType import ActivityType
from Projects.Executables.Pipelines.Inputs.InputConfig import InputConfig
from Projects.Executables.Pipelines.Inputs.Types.AlgorithmInput import AlgorithmInput


class AlgorithmDrivingInputActivity(AlgorithmInput, DrivingActivity):
    """
    Algorithm serves as input for itself.
    """

    def __init__(self, arguments: Arguments):
        # config and init commands
        device_config, file_data = self._get_init_configs(arguments)
        commands: List[Dict] = self._get_commands(**file_data)
        super(AlgorithmDrivingInputActivity, self).__init__(device_config=device_config, commands=commands)
        # init
        self.arguments: Arguments = arguments
        self.device_config: Dict = device_config

    def _get_input(self, **kwargs) -> DrivingActivity:
        # todo add commands calling self.add(nexxt_command) for adding next
        #  command for execution and calling self.start() method!
        pass

    def _get_commands(self, **file_data) -> List[Dict]:
        try:
            activity_type: str = file_data[InputConfig.ACTIVITY_TYPE_FIELD.value]

            if activity_type != ActivityType.DRIVING.value:
                raise ValueError(f'Missing {ActivityType.ACTIVITY_TYPE_FIELD.value} in file data!')

            return file_data[InputConfig.DRIVING_COMMANDS.value]

        except Exception as e:
            logging.error(f"Error during activity creation: {e}")
            return []
