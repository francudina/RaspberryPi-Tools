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
                 option_failure_penalty: float,
                 option_success_time_reward: float,
                 option_failure_time_penalty: float):
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
        # - likelihood rate
        self.option_success_reward: float = option_success_reward
        self.option_failure_penalty: float = option_failure_penalty
        # - time rate
        self.option_success_time_reward: float = option_success_time_reward
        self.option_failure_time_penalty: float = option_failure_time_penalty
        # - for success/failure rate storing/change
        self.execution_options: {} = self._driving_weighted_options()
        # - for success/failure time rate storing/change
        self.execution_time_options: {} = self._driving_time_options()
        self.execution_time_history: {} = {}

    def _pick_next_command(self) -> IDrivingCommand:
        while True:
            picked_option: Tuple[DirectionType, DrivingTurn] = self._roulette_wheel_selection(
                options=self.execution_options
            )

            payload = (picked_option[0], picked_option[1])

            # skip all black listed!
            if payload in self.direction_black_list:
                continue

            execution_time: timedelta = self._pick_command_execution_time(command=payload)
            return DrivingActivity.get_command_from_input(
                direction_type=picked_option[0],
                driving_turn=picked_option[1],
                execution_time=execution_time
            )

    def _pick_command_execution_time(self, command: Tuple[DirectionType, DrivingTurn]) -> timedelta:
        total_seconds: float = self.execution_time_options[command]
        return DrivingActivity.get_execution_time_from_seconds(total_seconds=total_seconds)

    def _use_execution_info(self, command: IDrivingCommand, compensation: bool) -> None:
        # if command failed
        direction: DirectionType = command.get_compensation_direction() if compensation \
            else command.direction_type
        turn: DrivingTurn = DrivingActivity.driving_turn_by_angle(command.wheel_angle)

        # direction & turn pair as command key/id
        payload = (direction, turn)

        # if payload is already in black list, skip
        # this is sometimes the case with compensation commands!
        if payload in self.direction_black_list:
            return

        # add total execution time to that command as history!
        if not compensation:
            # update execution time history
            self.execution_time_history.setdefault(payload, []).append(command.total_execution_time())

            # get avg execution time!
            avg_execution: timedelta = self._avg_timedelta_for_command(payload)
            logging.info(f"   > command avg execution time: {avg_execution}")

        # skip if command did not fail
        if command.status not in self.failed_status:

            # reward direction which was successful!
            self.__add_reward(command=payload, compensation=compensation)
            logging.debug("   > options update:\n{}".format(self.__options_to_string(self.execution_options)))
            logging.info("   > time options update:\n{}".format(self.__options_to_string(self.execution_time_options)))
            return

        # give penalty to direction which failed!
        self.__add_penalty(command=payload, compensation=compensation)
        logging.debug("   > options update:\n{}".format(self.__options_to_string(self.execution_options)))
        logging.info("   > time options update:\n{}".format(self.__options_to_string(self.execution_time_options)))

        # add to black list
        self.direction_black_list.append(payload)

        logging.info(f"   > command blacklisted: {payload}")
        logging.info(f"   > black list: {list(self.direction_black_list)}")

    def __options_to_string(self, options: {}) -> str:
        return json.dumps({f'({k[0].name}, {k[1].name})': v for k, v in options.items()}, indent=2)

    def __add_reward(self, command: Tuple[DirectionType, DrivingTurn], compensation: bool) -> None:
        # skip compensation reward
        if compensation or command not in self.execution_options.keys():
            return

        # 1. likelihood reward
        self.execution_options[command] += self.option_success_reward
        if self.execution_options[command] > 4:
            # restrict with the highest margin and reset
            self.execution_options[command] = 2

        # 2. time reward: multiply value
        self.execution_time_options[command] *= self.option_success_time_reward

    def __add_penalty(self, command: Tuple[DirectionType, DrivingTurn], compensation: bool) -> None:
        # skip compensation penalty
        if compensation or command not in self.execution_options.keys():
            return

        # 1. likelihood penalty
        self.execution_options[command] -= self.option_failure_penalty
        if self.execution_options[command] < 0:
            # reset value to low non-negative and non-zero number
            self.execution_options[command] = 0.05

        # 2. time reward: multiply value
        self.execution_time_options[command] *= self.option_failure_time_penalty

    def _avg_timedelta_for_command(self, command: Tuple[DirectionType, DrivingTurn]) -> timedelta:
        if command not in self.execution_time_history.keys():
            return timedelta(0)
        command_executions: List[timedelta] = self.execution_time_history[command]
        if len(command_executions) == 0:
            return timedelta(0)
        return sum(command_executions, timedelta(0)) / len(command_executions)
