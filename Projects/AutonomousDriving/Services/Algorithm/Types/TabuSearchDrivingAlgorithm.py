import json
import logging
from collections import deque
from typing import Tuple, List
from datetime import timedelta

from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithm import DrivingAlgorithm
from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithmType import DrivingAlgorithmType
from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.DrivingTurn import DrivingTurn
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
from Projects.Executables.ExecutablesStatus import ExecutablesStatus


class TabuSearchDrivingAlgorithm(DrivingAlgorithm):

    def __init__(self,
                 driving_activity: DrivingActivity,
                 max_execution_seconds: int,
                 tabu_queue_size: int,
                 option_success_reward: float,
                 option_failure_penalty: float):
        super().__init__(driving_activity, max_execution_seconds, DrivingAlgorithmType.TABU_SEARCH)
        # tabu lists
        self.direction_black_list: deque[Tuple[DirectionType, DrivingTurn]] = deque(maxlen=tabu_queue_size)
        # failed status list
        self.failed_status: List[ExecutablesStatus] = [
            ExecutablesStatus.BEFORE_COMPENSATION,
            # ExecutablesStatus.DONE_WITH_COMPENSATION,
            ExecutablesStatus.COMPENSATION_FAILED
        ]
        # options
        self.option_success_reward: float = option_success_reward
        self.option_failure_penalty: float = option_failure_penalty
        # - for success/failure rate storing/change
        self.execution_options: {} = self._driving_weighted_options()

    def _pick_next_command(self) -> IDrivingCommand:
        while True:
            picked_option: Tuple[DirectionType, DrivingTurn] = self._roulette_wheel_selection(
                options=self.execution_options
            )

            payload = (picked_option[0], picked_option[1])

            # skip all black listed!
            if payload in self.direction_black_list:
                continue

            execution_time: timedelta = DrivingActivity.get_execution_time('0:0:2')
            return DrivingActivity.get_command_from_input(
                direction_type=picked_option[0],
                driving_turn=picked_option[1],
                execution_time=execution_time
            )

    def _use_execution_info(self, command: IDrivingCommand, compensation: bool) -> None:
        # if command failed
        direction: DirectionType = command.get_compensation_direction() if compensation \
            else command.direction_type
        turn: DrivingTurn = DrivingActivity.driving_turn_by_angle(command.wheel_angle)

        payload = (direction, turn)

        # skip if command did not fail
        if command.status not in self.failed_status:
            # reward direction which was successful!
            self.execution_options[payload] += self.option_success_reward
            if self.execution_options[payload] > 10:
                # restrict with the highest margin and reset
                self.execution_options[payload] = 5

            logging.info("   > options update:\n{}".format(self.__options_to_string()))
            return

        # give penalty to direction which failed!
        self.execution_options[payload] -= self.option_failure_penalty
        if self.execution_options[payload] < 0:
            # reset value to low non-negative and non-zero number
            self.execution_options[payload] = 0.0001

        logging.info("   > options update:\n{}".format(self.__options_to_string()))

        # if payload is already in black list, skip
        # this is sometimes the case with compensation commands!
        if payload in self.direction_black_list:
            return

        # add to black list
        self.direction_black_list.append(payload)

        logging.info(f"   > command blacklisted: {payload}")
        logging.info(f"   > black list: {list(self.direction_black_list)}")

    def __options_to_string(self) -> str:
        return json.dumps({f'({k[0].name}, {k[1].name})': v for k, v in self.execution_options.items()}, indent=2)
