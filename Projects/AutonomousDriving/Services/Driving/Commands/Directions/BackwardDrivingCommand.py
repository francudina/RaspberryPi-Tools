import logging
from datetime import timedelta
from threading import Event

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.DrivingTurn import DrivingTurn
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingConfig import DrivingConfig
from Projects.Executables.Utils import TimeUtils


class BackwardDrivingCommand(IDrivingCommand):

    def __init__(self, wheel_angle: float, execution_time: timedelta):
        super(BackwardDrivingCommand, self).__init__(DirectionType.BACKWARD, wheel_angle)
        # init
        self.execution_time: timedelta = execution_time

    def start(self, **kwargs) -> bool:
        from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity

        turn: DrivingTurn = DrivingActivity.driving_turn_by_angle(self.wheel_angle)
        logging.info(f"  > direction {self.direction_type.name}, turn {turn.name} ... ({TimeUtils.current_time()})")
        return self.__execution(DirectionType.BACKWARD, method_name='start', **kwargs)

    def stop(self, **kwargs) -> bool:
        return True

    def compensate(self, **kwargs) -> bool:
        return self.__execution(self.get_compensation_direction(), method_name='compensate', **kwargs)

    def get_compensation_direction(self) -> DirectionType:
        return DirectionType.FORWARD

# private
    def __execution(self, direction_type: DirectionType, method_name: str, **kwargs) -> bool:
        self.__validate(**kwargs)

        from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
        activity: DrivingActivity = kwargs[DrivingConfig.COMMAND_ACTIVITY_ARG.value]

        try:
            # wheels to position
            activity.front_wheels_motor.new_result(input_angle=self.wheel_angle)

            expected_execution_time: timedelta = self.execution_time
            direction_event: Event = activity.get_obstacle_sensor_back_event()
            if method_name == 'compensate':
                # if "compensate" then compensate previous command with the
                # same amount of execution time but different direction!
                expected_execution_time = self.total_execution_time()
                # use different sensor if needed for compensation!
                direction_event = activity.get_obstacle_sensor_front_event()

            # start back wheels rotation
            passed: bool = activity.back_wheels_motor.new_result(
                execution_time=expected_execution_time,
                direction=direction_type,
                event=direction_event
            )

            return passed

        except Exception as e:
            logging.error(f'Error during {self.__class__.__name__}.{method_name}() method: {e}')
            return False

    def __validate(self, **kwargs):
        if DrivingConfig.COMMAND_ACTIVITY_ARG.value not in kwargs.keys():
            raise ValueError(f'{self.__class__.__name__} method must have '
                             f'DrivingActivity instance sent as method argument!')
