from datetime import datetime

import RPi.GPIO as GPIO

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.DrivingActivity import DrivingActivity
from Projects.Executables.External.Sensors.Variants.ObstacleSensor import ObstacleSensor


class DrivingObstacleSensor(ObstacleSensor):

    def __init__(self, activity: DrivingActivity, for_direction: DirectionType, pin_number: int,
                 board_mode: GPIO.BCM or GPIO.BOARD, with_callback: bool, bouncetime: int):
        super(DrivingObstacleSensor, self).__init__(
            pin_number=pin_number,
            board_mode=board_mode,
            with_callback=with_callback,
            bouncetime=bouncetime,
            callback_func=self._new_result_with_callback
        )
        # other
        self.activity: DrivingActivity = activity
        self.sensor_for_direction: DirectionType = for_direction

    def _new_result_with_callback(self, channel):
        # check channel state
        state = GPIO.input(channel)

        # if change was to the HIGH then skip!
        if state == GPIO.HIGH:
            return

        # check direction of the sensor to set the value!
        if self.sensor_for_direction == DirectionType.FORWARD:
            self.activity.get_obstacle_sensor_front_event().set()
        elif self.sensor_for_direction == DirectionType.BACKWARD:
            self.activity.get_obstacle_sensor_back_event().set()

        # set info that obstacle was found
        print(f"\t obstacle detected at {datetime.now().strftime('%H:%M:%S.%f')}")
