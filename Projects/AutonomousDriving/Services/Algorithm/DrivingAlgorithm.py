import random
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Tuple

from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithmType import DrivingAlgorithmType
from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.DrivingTurn import DrivingTurn
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
from Projects.Executables.Algorithm.IAlgorithm import IAlgorithm
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.Utils import TimeUtils


class DrivingAlgorithm(IAlgorithm, ABC):

    def __init__(self,
                 driving_activity: DrivingActivity,
                 max_execution_seconds: int,
                 driving_algorithm_type: DrivingAlgorithmType):
        super().__init__()
        # init
        self.driving_algorithm_type: DrivingAlgorithmType = driving_algorithm_type
        # activity
        self.driving_activity: DrivingActivity = driving_activity
        self.max_execution_seconds: int = max_execution_seconds
        # datetime
        self.start_time: datetime = None
        self.end_time: datetime = None

    def start(self, **kwargs) -> bool:

        logging.info(f"\n# Algorithm start: {self.__class__.__name__} ({TimeUtils.current_time()})")

        self.status = ExecutablesStatus.IN_PROGRESS
        self.start_time = datetime.now()

        while True:

            # check if time for execution passed
            delta: timedelta = datetime.now() - self.start_time
            if self.max_execution_seconds \
                    and delta.total_seconds() >= self.max_execution_seconds:

                logging.info(f"\n# MAX execution time reached, terminating ... ({TimeUtils.current_time()})")
                break

            logging.info("\n")
            command: IDrivingCommand = self._pick_next_command()
            if not command:
                continue

            logging.info(f"> command {command.activity_type}: START ({TimeUtils.current_time()})")

            command.status = ExecutablesStatus.IN_PROGRESS
            command.execution_start = datetime.now()
            started: bool = command.start(activity=self.driving_activity)
            command.execution_end = datetime.now()

            command.status = ExecutablesStatus.DONE if started \
                else ExecutablesStatus.BEFORE_COMPENSATION

            # reset events if needed after command execution!
            self.driving_activity.event_reset(command=command, is_compensation=False)

            # report execution e.g. results/status
            self._use_execution_info(command=command, compensation=False)

            if not started:
                logging.info(f" > command {command.activity_type} => FAILED ({TimeUtils.current_time()})")

                logging.info(f" \t> compensating command: START ({TimeUtils.current_time()})")
                compensated: bool = command.compensate(activity=self.driving_activity)
                logging.info(f" \t> compensating command: {'FAILED again' if not compensated else 'END'} "
                             f"({TimeUtils.current_time()})")

                # reset events if needed after command compensation!
                self.driving_activity.event_reset(command=command, is_compensation=True)

                command.status = ExecutablesStatus.DONE_WITH_COMPENSATION if compensated \
                    else ExecutablesStatus.COMPENSATION_FAILED

                self.status = command.status
                self.add(command)

                # use info from compensation
                self._use_execution_info(command=command, compensation=True)
                continue

            command.status = ExecutablesStatus.BEFORE_STOP
            ended: bool = command.stop(activity=self.driving_activity)
            command.status = ExecutablesStatus.FINISHED if ended \
                else ExecutablesStatus.STOP_FAILED

            self.status = command.status

            logging.info(f" > command {command.activity_type}: END ({TimeUtils.current_time()})")

            # history info
            self.add(command)

        self.end_time = datetime.now()
        self.status = ExecutablesStatus.FINISHED

        logging.info(f"\n\n < algorithm finished ({TimeUtils.current_time()})")
        return True

    def stop(self, **kwargs) -> bool:
        self.status = ExecutablesStatus.STOPPED
        return True

    def pause(self) -> bool:
        self.status = ExecutablesStatus.PAUSED
        return True

    def resume(self) -> bool:
        self.status = ExecutablesStatus.IN_PROGRESS
        return True

    @abstractmethod
    def _pick_next_command(self) -> IDrivingCommand:
        pass

    @abstractmethod
    def _use_execution_info(self, command: IDrivingCommand, compensation: bool) -> None:
        pass

    def _driving_weighted_options(self) -> {}:
        options: {} = self._create_default_options()
        tmp = list(options.items())
        random.shuffle(tmp)
        # sorting by value
        # return {k: v for k, v in sorted(options.items(), key=lambda item: -item[1])}
        return dict(tmp)

    def _create_default_options(self) -> {}:
        return {
            (DirectionType.FORWARD, DrivingTurn.NONE): 0.5,
            (DirectionType.FORWARD, DrivingTurn.LEFT): 0.25,
            (DirectionType.FORWARD, DrivingTurn.RIGHT): 0.25,

            (DirectionType.BACKWARD, DrivingTurn.NONE): 0.35,
            (DirectionType.BACKWARD, DrivingTurn.LEFT): 0.25,
            (DirectionType.BACKWARD, DrivingTurn.RIGHT): 0.25,

            (DirectionType.NONE, DrivingTurn.NONE): 0.3
        }

    def _driving_time_options(self) -> {}:
        return {
            (DirectionType.FORWARD, DrivingTurn.NONE): 3,
            (DirectionType.FORWARD, DrivingTurn.LEFT): 3,
            (DirectionType.FORWARD, DrivingTurn.RIGHT): 3,

            (DirectionType.BACKWARD, DrivingTurn.NONE): 2,
            (DirectionType.BACKWARD, DrivingTurn.LEFT): 2,
            (DirectionType.BACKWARD, DrivingTurn.RIGHT): 2,

            (DirectionType.NONE, DrivingTurn.NONE): 1
        }

    def _roulette_wheel_selection(self, options: {}) -> Tuple[DirectionType, DrivingTurn]:
        max_val: float = sum(probability for _, probability in options.items())
        pick: float = random.uniform(0, max_val)
        current: float = 0
        for direction_turn_pair, probability in options.items():
            upper: float = current + probability
            if current < pick <= upper:
                return direction_turn_pair
            current = upper
