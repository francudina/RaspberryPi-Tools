import logging
from datetime import timedelta

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingConfig import DrivingConfig


class BackwardDrivingCommand(IDrivingCommand):

    def __init__(self, wheel_angle: float, execution_time: timedelta):
        super(BackwardDrivingCommand, self).__init__(DirectionType.BACKWARD, wheel_angle)
        # init
        self.execution_time: timedelta = execution_time

    def start(self, **kwargs) -> bool:
        print(f"  > direction {self.direction_type} ...")
        return self.__execution(DirectionType.BACKWARD, method_name='start', **kwargs)

    def stop(self, **kwargs) -> bool:
        return True

    def compensate(self, **kwargs) -> bool:
        return self.__execution(DirectionType.FORWARD, method_name='compensate', **kwargs)

    # private
    def __execution(self, direction_type: DirectionType, method_name: str, **kwargs) -> bool:
        self.__validate(**kwargs)

        from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
        activity: DrivingActivity = kwargs[DrivingConfig.COMMAND_ACTIVITY_ARG.value]

        try:
            # wheels to position
            # activity.front_wheels_motor.start()
            activity.front_wheels_motor.new_result(input_angle=self.wheel_angle)
            # activity.front_wheels_motor.stop()
            # start back wheels rotation
            # activity.back_wheels_motor.start()
            activity.back_wheels_motor.new_result(execution_time=self.execution_time, direction=direction_type)
            # activity.back_wheels_motor.stop()
            return True
        except Exception as e:
            logging.error(f'Error during {self.__class__.__name__}.{method_name}() method: {e}')
            return False

    def __validate(self, **kwargs):
        if DrivingConfig.COMMAND_ACTIVITY_ARG.value not in kwargs.keys():
            raise ValueError(f'{self.__class__.__name__} method must have DrivingActivity instance sent as method argument!')
