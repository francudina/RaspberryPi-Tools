import logging
import time
from datetime import timedelta

import RPi.GPIO as GPIO
from typing import Any

from Projects.Executables.External.IExternalService import IExternalService


class ExternalLED(IExternalService):

    def __init__(self, pin_number: int, board_mode: GPIO.BCM or GPIO.BOARD):
        super(ExternalLED, self).__init__(pin_number, GPIO.OUT, board_mode)

    def new_result(self, **kwargs) -> Any:
        return True

    def start(self, **kwargs) -> bool:
        return self.__configure()

    def pause(self, **kwargs) -> bool:
        try:
            GPIO.output(self.pin_number, GPIO.LOW)
            return True
        except Exception as e:
            return False

    def resume(self, **kwargs) -> bool:
        try:
            GPIO.output(self.pin_number, GPIO.HIGH)
            return True
        except Exception as e:
            return False

    def stop(self, **kwargs) -> bool:
        try:
            GPIO.output(self.pin_number, GPIO.LOW)
            GPIO.cleanup(self.pin_number)
            return True
        except Exception as e:
            logging.error(f'Error in ExternalLED.__configure() method: {e}')
            return False

    # private
    def __configure(self) -> bool:
        try:
            GPIO.setmode(self.board_mode)
            GPIO.setwarnings(False)

            GPIO.setup(self.pin_number, self.pin_direction)
            GPIO.output(self.pin_number, GPIO.HIGH)

            return True
        except Exception as e:
            logging.error(f'Error in ExternalLED.__configure() method: {e}')
            return False
