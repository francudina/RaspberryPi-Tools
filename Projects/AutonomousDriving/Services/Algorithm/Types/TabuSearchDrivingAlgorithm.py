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
                 tabu_queue_size: int):
        super().__init__(driving_activity, max_execution_seconds, DrivingAlgorithmType.TABU_SEARCH)
        # tabu lists
        self.direction_black_list: deque[Tuple[DirectionType, DrivingTurn]] = deque(maxlen=tabu_queue_size)
        # failed status list
        self.failed_status: List[ExecutablesStatus] = [
            ExecutablesStatus.BEFORE_COMPENSATION,
            ExecutablesStatus.DONE_WITH_COMPENSATION,
            ExecutablesStatus.COMPENSATION_FAILED
        ]

    def _pick_next_command(self) -> IDrivingCommand:
        options: {} = self._driving_weighted_options()
        while True:
            picked_option: Tuple[DirectionType, DrivingTurn] = self._roulette_wheel_selection(options=options)

            payload = (picked_option[0], picked_option[1])

            logging.info(f" > black list: {list(self.direction_black_list)}")
            # skip all black listed!
            if payload in self.direction_black_list:
                logging.info(f" > command skipped: {payload}")
                continue

            logging.info(f" > command: {payload}")

            execution_time: timedelta = DrivingActivity.get_execution_time('0:0:2')
            return DrivingActivity.get_command_from_input(
                direction_type=picked_option[0],
                driving_turn=picked_option[1],
                execution_time=execution_time
            )

    def _use_execution_info(self, command: IDrivingCommand, compensation: bool) -> None:
        # skip if command did not fail
        if command.status not in self.failed_status:
            return

        # if command failed
        direction: DirectionType = command.get_compensation_direction() if compensation \
            else command.direction_type
        turn: DrivingTurn = DrivingActivity.driving_turn_by_angle(command.wheel_angle)

        payload = (direction, turn)

        # if payload is already in black list, skip
        if payload in self.direction_black_list:
            return

        # add to black list
        self.direction_black_list.append(payload)

        logging.info(f" > command blacklisted: {payload}")
        logging.info(f" > black list: {list(self.direction_black_list)}")
