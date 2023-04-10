import time
import logging
from datetime import timedelta

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingConfig import DrivingConfig
from Projects.Executables.External.Motors.MotorConfig import MotorConfig
from Projects.Executables.Utils import TimeUtils


class NoneDrivingCommand(IDrivingCommand):

    def __init__(self, execution_time: timedelta):
        super(NoneDrivingCommand, self).__init__(DirectionType.NONE, MotorConfig.SERVO_STARTING_POINT.value)
        # init
        self.execution_time: timedelta = execution_time

    def start(self, **kwargs) -> bool:
        print(f"  > direction {self.direction_type} ...")
        return self.__execution(method_name='start', **kwargs)

    def stop(self, **kwargs) -> bool:
        return True

    def compensate(self, **kwargs) -> bool:
        return True

# private
    def __execution(self, method_name: str, **kwargs) -> bool:
        self.__validate(**kwargs)

        from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
        activity: DrivingActivity = kwargs[DrivingConfig.COMMAND_ACTIVITY_ARG.value]

        try:
            # wheels to position
            activity.front_wheels_motor.new_result(input_angle=self.wheel_angle)
            # time.sleep(self.execution_time.total_seconds())
            interrupted: bool = TimeUtils.blocking_sleep(self.execution_time.total_seconds())

            # True only if operation wasn't interrupted
            return not interrupted

        except Exception as e:
            logging.error(f'Error during {self.__class__.__name__}.{method_name}() method: {e}')
            return False

    def __validate(self, **kwargs):
        if DrivingConfig.COMMAND_ACTIVITY_ARG.value not in kwargs.keys():
            raise ValueError(f'{self.__class__.__name__} method must have '
                             f'DrivingActivity instance sent as method argument!')
