from typing import Tuple
from datetime import timedelta

from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithm import DrivingAlgorithm
from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithmType import DrivingAlgorithmType
from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.DrivingTurn import DrivingTurn
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity


class RandomDrivingAlgorithm(DrivingAlgorithm):

    def __init__(self,
                 driving_activity: DrivingActivity,
                 max_execution_seconds: int):
        super().__init__(driving_activity, max_execution_seconds, DrivingAlgorithmType.RANDOM)
        # options
        self.driving_options: {} = self._driving_weighted_options()

    def _pick_next_command(self) -> IDrivingCommand:
        picked_option: Tuple[DirectionType, DrivingTurn] = self._roulette_wheel_selection(
            options=self.driving_options
        )
        execution_time: timedelta = DrivingActivity.get_execution_time('0:0:2')
        return DrivingActivity.get_command_from_input(
            direction_type=picked_option[0],
            driving_turn=picked_option[1],
            execution_time=execution_time
        )

    def _use_execution_info(self, command: IDrivingCommand) -> None:
        # ignoring method calls
        pass
