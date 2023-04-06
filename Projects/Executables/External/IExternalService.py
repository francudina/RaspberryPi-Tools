import logging
import RPi.GPIO as GPIO
from abc import abstractmethod
from typing import Any

from Projects.Executables.IExecutable import IExecutable


class IExternalService(IExecutable):

    def __init__(self, pin_number: int, pin_direction: GPIO.OUT or GPIO.IN, board_mode: GPIO.BCM or GPIO.BOARD):
        super(IExternalService, self).__init__()
        # input values
        self.pin_number: int = pin_number
        self.pin_direction = pin_direction
        self.board_mode = board_mode

# methods
    # callback method for sensor readings!
    @abstractmethod
    def new_result(self, **kwargs) -> Any:
        pass

    def stop(self, **kwargs) -> bool:
        # doc: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
        GPIO.cleanup(self.pin_number)
        return True
