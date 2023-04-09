import RPi.GPIO as GPIO
from datetime import datetime
from typing import List, Dict, Callable, Any

from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.External.Sensors.ISensor import ISensor


class ObstacleSensor(ISensor):

    def __init__(self, pin_number: int, board_mode: GPIO.BCM or GPIO.BOARD, with_callback: bool, bouncetime: int):
        # if with_callback then sensor gets value with GPIO.LOW value, so GPIO.FALLING is set!
        super(ObstacleSensor, self).__init__(
            pin_number,
            GPIO.IN,
            board_mode,
            with_callback,
            bouncetime,
            GPIO.PUD_UP,
            GPIO.FALLING,
            self._new_result_with_callback
        )

    def _new_result_with_callback(self, channel):
        state = GPIO.input(channel)
        if state == GPIO.LOW:
            print(f"\t+ event detected on channel '{channel}' at {datetime.now().strftime('%H:%M:%S.%f')}")

