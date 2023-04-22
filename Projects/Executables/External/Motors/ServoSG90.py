import time
import logging
import RPi.GPIO as GPIO
from typing import Any

from Projects.Executables.External.IExternalService import IExternalService
from Projects.Executables.External.Motors.MotorConfig import MotorConfig
from Projects.Executables.Utils import TimeUtils


class ServoSG90(IExternalService):

    def __init__(self, pin_number: int, board_mode: GPIO.BCM or GPIO.BOARD):
        super(ServoSG90, self).__init__(pin_number, GPIO.OUT, board_mode)
        # input values
        self.pwm_channel = None  # configured later in configure() method

# methods
    # public
    def new_result(self, **kwargs) -> Any:
        if MotorConfig.SERVO_INPUT_ANGLE.value not in kwargs.keys():
            raise ValueError(f'ServoSG90.new_result(**kwargs) must have '
                             f'{MotorConfig.SERVO_INPUT_ANGLE.value} key specified!')
        try:
            input_value: float = float(kwargs[MotorConfig.SERVO_INPUT_ANGLE.value])
            next_cycle = self.__calculate_angle_cycle(input_value)
            self.pwm_channel.ChangeDutyCycle(next_cycle)
            interrupted: bool = TimeUtils.blocking_sleep(1)

            return True, next_cycle
        except Exception as e:
            logging.error(f'Error in ServoSG90.new_result(**kwargs) method! Message: {e}')
            return False, None

    def start(self, **kwargs) -> bool:
        return self.__configure()

    def stop(self, **kwargs) -> bool:
        try:
            self.pwm_channel.stop()

            GPIO.cleanup(self.pin_number)
            return True
        except:
            return False

    # private
    def __configure(self) -> bool:
        try:
            GPIO.setmode(self.board_mode)

            GPIO.setup(self.pin_number, self.pin_direction)
            GPIO.output(self.pin_number, GPIO.LOW)

            self.pwm_channel = GPIO.PWM(self.pin_number, int(MotorConfig.SERVO_MOTOR_Hz.value))
            self.pwm_channel.start(0)

            return True
        except Exception as e:
            logging.error(f'Error in ServoSG90.__configure() method: {e}')
            return False

    def __calculate_angle_cycle(self, angle):
        min_angle = int(MotorConfig.SERVO_MIN_ANGLE.value)
        max_angle = int(MotorConfig.SERVO_MAX_ANGLE.value)

        to_low = float(MotorConfig.SERVO_MIN_DUTY.value)
        to_high = float(MotorConfig.SERVO_MAX_DUTY.value)

        if angle < min_angle:
            angle = min_angle
        elif angle > max_angle:
            angle = max_angle

        return (to_high - to_low) * (angle - min_angle) / (max_angle - min_angle) + to_low
