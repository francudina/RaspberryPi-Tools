import logging
from time import sleep
import RPi.GPIO as GPIO
from typing import Any
from datetime import timedelta

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.Executables.External.IExternalService import IExternalService
from Projects.Executables.External.Motors.MotorConfig import MotorConfig


class DriveMotor(IExternalService):

    def __init__(self,
                 pin_number_in1: int,
                 pin_number_in2: int,
                 pin_number_pwm: int,
                 pin_number_sby: int,
                 board_mode: GPIO.BCM or GPIO.BOARD):
        super(DriveMotor, self).__init__(-1, GPIO.OUT, board_mode)
        # input values
        # - pins
        self.pin_number_in1: int = pin_number_in1
        self.pin_number_in2: int = pin_number_in2
        self.pin_number_pwm: int = pin_number_pwm
        self.pin_number_sby: int = pin_number_sby
        # - other
        self.pwm_channel = None  # configured later in configure() method

    def new_result(self, **kwargs) -> Any:
        self.__validate(**kwargs)
        execution_time: timedelta = kwargs[MotorConfig.BASIC_MOTOR_EXECUTION_TIME.value]
        direction: DirectionType = kwargs[MotorConfig.BASIC_MOTOR_DIRECTION.value]
        return self.__execute_in_direction(direction, execution_time)

    def start(self, **kwargs) -> bool:
        return self.__configure()

    def stop(self, **kwargs) -> bool:
        try:
            self.pwm_channel.stop()

            GPIO.cleanup(self.pin_number_in1)
            GPIO.cleanup(self.pin_number_in2)
            GPIO.cleanup(self.pin_number_pwm)
            GPIO.cleanup(self.pin_number_sby)
            return True
        except:
            return False

    # private
    def __configure(self) -> bool:
        try:
            GPIO.setmode(self.board_mode)
            GPIO.setwarnings(False)

            GPIO.setup(self.pin_number_in1, self.pin_direction)
            GPIO.setup(self.pin_number_in2, self.pin_direction)
            GPIO.setup(self.pin_number_pwm, self.pin_direction)
            GPIO.setup(self.pin_number_sby, self.pin_direction)

            self.pwm_channel = GPIO.PWM(self.pin_number_pwm, int(MotorConfig.BASIC_MOTOR_Hz.value))
            self.pwm_channel.start(int(MotorConfig.BASIC_STARTING_POINT.value))

            return True
        except Exception as e:
            logging.error(f'Error in DriveMotor.__configure() method: {e}')
            return False

    def __execute_in_direction(self, direction: DirectionType, execution_time: timedelta):
        try:
            if direction == DirectionType.FORWARD:
                # forward
                in1 = GPIO.HIGH
                in2 = GPIO.LOW
            elif direction == DirectionType.BACKWARD:
                # backward
                in1 = GPIO.LOW
                in2 = GPIO.HIGH
            else:
                # None
                in1 = GPIO.LOW
                in2 = GPIO.LOW

            # motor start
            GPIO.output(self.pin_number_sby, GPIO.HIGH)

            GPIO.output(self.pin_number_in1, in1)
            GPIO.output(self.pin_number_in2, in2)
            self.pwm_channel.ChangeDutyCycle(int(MotorConfig.BASIC_MOTOR_SPEED.value))

            # execution time ...
            sleep(execution_time.total_seconds())

            # motor stop
            GPIO.output(self.pin_number_sby, GPIO.LOW)

            return True
        except:
            return False

    def __validate(self, **kwargs):
        if MotorConfig.BASIC_MOTOR_EXECUTION_TIME.value not in kwargs.keys():
            raise ValueError(f'DriveMotor.new_result(**kwargs) must have '
                             f'{MotorConfig.BASIC_MOTOR_EXECUTION_TIME.value} key specified!')
        if MotorConfig.BASIC_MOTOR_DIRECTION.value not in kwargs.keys():
            raise ValueError(f'DriveMotor.new_result(**kwargs) must have '
                             f'{MotorConfig.BASIC_MOTOR_DIRECTION.value} key specified!')
