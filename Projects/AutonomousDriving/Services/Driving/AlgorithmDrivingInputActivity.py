import logging
from typing import List, Dict

from Projects.AutonomousDriving.Config.Arguments import Arguments
from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithm import DrivingAlgorithm
from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithmType import DrivingAlgorithmType
from Projects.AutonomousDriving.Services.Algorithm.Types.RandomDrivingAlgorithm import RandomDrivingAlgorithm
from Projects.AutonomousDriving.Services.Algorithm.Types.TabuSearchDrivingAlgorithm import TabuSearchDrivingAlgorithm
from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
from Projects.Executables.Activities.ActivityType import ActivityType
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.Pipelines.Inputs.InputConfig import InputConfig
from Projects.Executables.Pipelines.Inputs.Types.AlgorithmInput import AlgorithmInput


class AlgorithmDrivingInputActivity(DrivingActivity, AlgorithmInput):
    """
    Algorithm serves as input for itself.
    """

    def __init__(self, arguments: Arguments):
        # config and init commands
        device_config, file_data = self._get_init_configs(arguments)
        commands: List[Dict] = self._get_commands(**file_data)
        super(AlgorithmDrivingInputActivity, self).__init__(
            pipeline_input_type=arguments.pipeline_input,
            device_config=device_config,
            commands=commands)
        # init
        self.arguments: Arguments = arguments
        self.device_config: Dict = device_config
        self.algorithm_type: DrivingAlgorithmType = self.arguments.algorithm

    def start(self, **kwargs) -> bool:

        passed: bool = super().start(**kwargs)
        # check status
        if self.status == ExecutablesStatus.FAILED:
            return False

        # start with algorithm process!
        algorithm: DrivingAlgorithm = self._choose_algorithm()
        started: bool = algorithm.start()
        # stopped: bool = algorithm.stop()

        # update algorithm input status!
        self.status = algorithm.status

        # return started and stopped
        return started

    def compensate(self, **kwargs) -> bool:
        """
        Compensate not implemented in this case.
        :param kwargs:
        :return:
        """
        return True

    def _get_input(self, **kwargs) -> DrivingActivity:
        """
        At this point all init commands were added to Activity, so we don't need to add them manually now.
        But, it is needed to start algorithm if there is no init commands.

        :param kwargs: potential input params
        :return: current AlgorithmDrivingInputActivity activity
        """
        return self

    def _get_commands(self, **file_data) -> List[Dict]:
        try:
            if InputConfig.ACTIVITY_TYPE_FIELD.value not in file_data.keys():
                return []

            activity_type: str = file_data[InputConfig.ACTIVITY_TYPE_FIELD.value]

            if activity_type != ActivityType.DRIVING.value:
                raise ValueError(f'Missing {ActivityType.ACTIVITY_TYPE_FIELD.value} in file data!')

            return file_data[InputConfig.DRIVING_COMMANDS.value]

        except Exception as e:
            logging.error(f"Error during activity creation: {e}")
            return []

    def _choose_algorithm(self) -> DrivingAlgorithm:
        if self.arguments.algorithm == DrivingAlgorithmType.RANDOM:
            return RandomDrivingAlgorithm(
                driving_activity=self,
                max_execution_seconds=self.arguments.max_execution_seconds
            )
        elif self.arguments.algorithm == DrivingAlgorithmType.TABU_SEARCH:
            return TabuSearchDrivingAlgorithm(
                driving_activity=self,
                max_execution_seconds=self.arguments.max_execution_seconds,
                tabu_queue_size=self.arguments.tabu_queue_size,
                option_success_reward=self.arguments.option_success_reward,
                option_failure_penalty=self.arguments.option_failure_penalty,
                option_success_time_reward=self.arguments.option_success_time_reward,
                option_failure_time_penalty=self.arguments.option_failure_time_penalty,
            )
        else:
            raise ValueError(f'Wrong/Not supported DrivingAlgorithmType sent: {self.arguments.algorithm}')
