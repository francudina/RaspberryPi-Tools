from enum import Enum


class MotorConfig(Enum):

    # servo
    # - motor
    SERVO_ERROR_OFFSET = 0.5
    SERVO_MIN_DUTY = 2.5 + SERVO_ERROR_OFFSET  # duty cycle for 0 degrees
    SERVO_MAX_DUTY = 12.5 + SERVO_ERROR_OFFSET  # duty cycle for 180 degrees
    SERVO_MIN_ANGLE = 0  # degrees
    SERVO_MAX_ANGLE = 180  # degrees

    SERVO_MOTOR_Hz = 50
    SERVO_LEFT_TURN_POINT = 130.0
    SERVO_STARTING_POINT = 60.0
    SERVO_RIGHT_TURN_POINT = 0.0

    SERVO_STARTING_POINT_ANGLE_DELTA = 5.0

    BASIC_MOTOR_Hz = 100
    BASIC_STARTING_POINT = 0.0

    BASIC_MOTOR_SPEED = 50

    # - params
    # - servo
    SERVO_INPUT_ANGLE = 'input_angle'
    # - servo
    BASIC_MOTOR_EXECUTION_TIME = 'execution_time'
    BASIC_MOTOR_DIRECTION = 'direction'
    BASIC_MOTOR_EVENT = 'event'
