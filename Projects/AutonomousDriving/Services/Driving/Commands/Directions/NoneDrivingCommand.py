import logging
from datetime import timedelta, datetime

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.DrivingTurn import DrivingTurn
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingConfig import DrivingConfig
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.External.Motors.MotorConfig import MotorConfig
from Projects.Executables.Utils import TimeUtils


class NoneDrivingCommand(IDrivingCommand):

    def __init__(self, execution_time: timedelta):
        super(NoneDrivingCommand, self).__init__(DirectionType.NONE, MotorConfig.SERVO_STARTING_POINT.value)
        # init
        self.execution_time: timedelta = execution_time

    def start(self, **kwargs) -> bool:
        from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity

        turn: DrivingTurn = DrivingActivity.driving_turn_by_angle(self.wheel_angle)
        logging.info(f"  > direction {self.direction_type.name}, turn {turn.name} ... ({TimeUtils.current_time()})")
        return self.__execution(method_name='start', **kwargs)

    def stop(self, **kwargs) -> bool:
        return True

    def compensate(self, **kwargs) -> bool:
        return True

    def get_compensation_direction(self) -> DirectionType:
        return DirectionType.NONE

# private
    def __execution(self, method_name: str, **kwargs) -> bool:
        self.__validate(**kwargs)

        from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
        activity: DrivingActivity = kwargs[DrivingConfig.COMMAND_ACTIVITY_ARG.value]

        try:
            # wheels to position
            activity.front_wheels_motor.new_result(input_angle=self.wheel_angle)

            # no usage of sensors
            if not activity.using_front_sensor and not activity.using_back_sensor:
                interrupted: bool = TimeUtils.blocking_sleep(self.execution_time.total_seconds())
                return not interrupted

            # calculate nonblocking thread sleep for event listeners!
            sleep_between_sec: float = self.execution_time.total_seconds()
            if activity.using_front_sensor:
                sleep_between_sec /= 50
            if activity.using_back_sensor:
                sleep_between_sec /= 50

            interrupted_front, interrupted_back = False, False
            start: datetime = datetime.now()
            while (datetime.now() - start).total_seconds() < self.execution_time.total_seconds():

                if activity.using_front_sensor:
                    # sleep on front sensor!
                    interrupted_front = TimeUtils.nonblocking_sleep(
                        sleep_between_sec,
                        activity.get_obstacle_sensor_front_event()
                    )
                    # but check also back sensor if both occurred!
                    interrupted_back = activity.get_obstacle_sensor_back_event().is_set()
                    break

                if activity.using_back_sensor:
                    # sleep on back sensor!
                    interrupted_back = TimeUtils.nonblocking_sleep(
                        sleep_between_sec,
                        activity.get_obstacle_sensor_back_event()
                    )
                    # but check also front sensor if both occurred!
                    interrupted_front = activity.get_obstacle_sensor_front_event().is_set()
                    break

            # if none of them is triggered
            if not interrupted_front and not interrupted_back:
                return True

            # stay in place/do nothing if both are triggered
            if interrupted_front and interrupted_back:
                logging.info(f"   > multiple obstacles detected while waiting: NO ACTION")
                return False

            # execute 2 seconds action if sensors triggered!
            execution_time: timedelta = DrivingActivity.get_execution_time('0:0:2')

            # pick direction
            direction: DirectionType = DirectionType.BACKWARD if interrupted_front \
                else DirectionType.FORWARD

            obstacle_position: str = 'FRONT' if interrupted_front else 'BACK'
            logging.info(f"   > {obstacle_position} obstacle detected obstacle while waiting, "
                         f"executing direction: {direction.name} ({TimeUtils.current_time()})")

            command: IDrivingCommand = DrivingActivity.get_command_from_input(
                direction_type=direction,
                driving_turn=DrivingTurn.NONE,  # turn if fixed to None
                execution_time=execution_time
            )

            # execute command
            command.status = ExecutablesStatus.IN_PROGRESS
            command.execution_start = datetime.now()
            started: bool = command.start(activity=activity)
            command.execution_end = datetime.now()

            command.status = ExecutablesStatus.FINISHED if started \
                else ExecutablesStatus.FAILED

            logging.info(f"   > command execution status: {command.status.name} ({TimeUtils.current_time()})")

            # True only if operation wasn't interrupted
            return started

        except Exception as e:
            logging.error(f'Error during {self.__class__.__name__}.{method_name}() method: {e}')
            return False

    def __execute_command(self, command: IDrivingCommand) -> bool:
        pass

    def __validate(self, **kwargs):
        if DrivingConfig.COMMAND_ACTIVITY_ARG.value not in kwargs.keys():
            raise ValueError(f'{self.__class__.__name__} method must have '
                             f'DrivingActivity instance sent as method argument!')
