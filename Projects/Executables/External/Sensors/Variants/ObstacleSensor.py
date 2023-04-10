from abc import ABC
from typing import Callable

import RPi.GPIO as GPIO

from Projects.Executables.External.Sensors.ISensor import ISensor


class ObstacleSensor(ISensor, ABC):

    def __init__(self, pin_number: int,
                 board_mode: GPIO.BCM or GPIO.BOARD, with_callback: bool, bouncetime: int, callback_func: Callable):
        # if with_callback then sensor gets value with GPIO.LOW value, so GPIO.FALLING is set!
        super(ObstacleSensor, self).__init__(
            pin_number,
            GPIO.IN,
            board_mode,
            with_callback,
            bouncetime,
            GPIO.PUD_UP,
            GPIO.FALLING,
            callback_func
        )
