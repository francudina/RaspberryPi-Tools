from typing import Any

import RPi.GPIO as GPIO


class DrivingUtils:

    @staticmethod
    def get_board_mode(board_mode: str) -> Any:
        if board_mode == "GPIO.BCM":
            return GPIO.BCM
        elif board_mode == "GPIO.BOARD":
            return GPIO.BOARD
        else:
            return None

    @staticmethod
    def get_pin_direction(pin_direction: str) -> Any:
        if pin_direction == "GPIO.IN":
            return GPIO.IN
        elif pin_direction == "GPIO.OUT":
            return GPIO.OUT
        else:
            return None

    @staticmethod
    def get_voltage_level(voltage_level: str) -> Any:
        if voltage_level == "GPIO.HIGH":
            return GPIO.HIGH
        elif voltage_level == "GPIO.LOW":
            return GPIO.LOW
        else:
            return None
