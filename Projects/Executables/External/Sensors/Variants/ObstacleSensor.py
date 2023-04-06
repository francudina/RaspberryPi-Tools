import RPi.GPIO as GPIO
from typing import List, Dict, Callable, Any

from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.External.Sensors.ISensor import ISensor


class ObstacleSensor(ISensor):

    def __init__(self, pin_number: int, board_mode: GPIO.BCM or GPIO.BOARD, with_callback: bool):
        # if with_callback then sensor gets value with GPIO.LOW value, so GPIO.FALLING is set!
        super(ObstacleSensor, self).__init__(pin_number, GPIO.IN,
                                             board_mode, with_callback, GPIO.FALLING, self.new_result)

    def new_result(self, **kwargs) -> Any:
        return super().new_result(**kwargs)
