from datetime import datetime, timedelta
from typing import List, Dict

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.AutonomousDriving.Services.Driving.Commands.Directions.BackwardDrivingCommand import \
    BackwardDrivingCommand
from Projects.AutonomousDriving.Services.Driving.Commands.Directions.ForwardDrivingCommand import ForwardDrivingCommand
from Projects.AutonomousDriving.Services.Driving.Commands.Directions.NoneDrivingCommand import NoneDrivingCommand
from Projects.AutonomousDriving.Services.Driving.Commands.DrivingTurn import DrivingTurn
from Projects.AutonomousDriving.Services.Driving.Commands.IDrivingCommand import IDrivingCommand
from Projects.AutonomousDriving.Services.Driving.DrivingConfig import DrivingConfig
from Projects.AutonomousDriving.Services.Driving.DrivingUtils import DrivingUtils
from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.External.LightBulbs.ExternalLED import ExternalLED
from Projects.Executables.External.Motors.DriveMotor import DriveMotor
from Projects.Executables.External.Motors.MotorConfig import MotorConfig
from Projects.Executables.External.Motors.ServoSG90 import ServoSG90
from Projects.Executables.External.Sensors.Variants.ObstacleSensor import ObstacleSensor
from Projects.Executables.Pipelines.Inputs.InputConfig import InputConfig
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType


class DrivingActivity(IActivity):

    def __init__(self, pipeline_input_type: PipelineInputType, **driving_config):
        input_commands: List[IDrivingCommand] = DrivingActivity.get_commands(**driving_config)
        super(DrivingActivity, self).__init__(pipeline_input_type, input_commands)
        # init vars
        self.use_sensors: bool = driving_config[InputConfig.DRIVING_USE_SENSORS_FIELD.value]
        self.using_front_sensor: bool = driving_config[DrivingConfig.OBSTACLE_FRONT_SENSOR.value][DrivingConfig.OBSTACLE_SENSOR_USING_SENSOR.value]
        self.using_back_sensor: bool = driving_config[DrivingConfig.OBSTACLE_BACK_SENSOR.value][DrivingConfig.OBSTACLE_SENSOR_USING_SENSOR.value]
        self.use_LEDs: bool = driving_config[InputConfig.DRIVING_USE_LEDs_FIELD.value]
        self.__execution_start: datetime = datetime.now()
        # - motors
        self.front_wheels_motor: ServoSG90 = ServoSG90(
            pin_number=driving_config[DrivingConfig.SERVO_CONFIG.value][DrivingConfig.SERVO_PIN_NUMBER.value],
            board_mode=DrivingUtils.get_board_mode(driving_config[DrivingConfig.SERVO_CONFIG.value][DrivingConfig.SERVO_BOARD_MODE.value])
        )
        self.front_wheels_motor.start()
        self.back_wheels_motor: DriveMotor = DriveMotor(
            pin_number_in1=driving_config[DrivingConfig.MOTOR_CONFIG.value][DrivingConfig.MOTOR_PIN_NUMBER_IN1.value],
            pin_number_in2=driving_config[DrivingConfig.MOTOR_CONFIG.value][DrivingConfig.MOTOR_PIN_NUMBER_IN2.value],
            pin_number_pwm=driving_config[DrivingConfig.MOTOR_CONFIG.value][DrivingConfig.MOTOR_PIN_NUMBER_PWM.value],
            pin_number_sby=driving_config[DrivingConfig.MOTOR_CONFIG.value][DrivingConfig.MOTOR_PIN_NUMBER_SBY.value],
            board_mode=DrivingUtils.get_board_mode(driving_config[DrivingConfig.MOTOR_CONFIG.value][DrivingConfig.MOTOR_BOARD_MODE.value]),
        )
        self.back_wheels_motor.start()
        # - sensors
        if self.use_sensors:
            # - sensors.front
            if self.using_front_sensor:
                front_sensor: {} = driving_config[DrivingConfig.OBSTACLE_FRONT_SENSOR.value]
                self.front_obstacle_sensor: ObstacleSensor = ObstacleSensor(
                    pin_number=front_sensor[DrivingConfig.OBSTACLE_SENSOR_PIN_NUMBER.value],
                    board_mode=DrivingUtils.get_board_mode(front_sensor[DrivingConfig.OBSTACLE_SENSOR_BOARD_MODE.value]),
                    with_callback=front_sensor[DrivingConfig.OBSTACLE_SENSOR_WITH_CALLBACK.value],
                    bouncetime=front_sensor[DrivingConfig.OBSTACLE_SENSOR_BOUNCETIME.value]
                )
                self.front_obstacle_sensor.start()
            else:
                self.front_obstacle_sensor: ObstacleSensor = None
            # - sensors.back
            if self.using_back_sensor:
                back_sensor: {} = driving_config[DrivingConfig.OBSTACLE_BACK_SENSOR.value]
                self.back_obstacle_sensor: ObstacleSensor = ObstacleSensor(
                    pin_number=back_sensor[DrivingConfig.OBSTACLE_SENSOR_PIN_NUMBER.value],
                    board_mode=DrivingUtils.get_board_mode(back_sensor[DrivingConfig.OBSTACLE_SENSOR_BOARD_MODE.value]),
                    with_callback=back_sensor[DrivingConfig.OBSTACLE_SENSOR_WITH_CALLBACK.value],
                    bouncetime=back_sensor[DrivingConfig.OBSTACLE_SENSOR_BOUNCETIME.value]
                )
                self.back_obstacle_sensor.start()
            else:
                self.back_obstacle_sensor: ObstacleSensor = None
        else:
            self.front_obstacle_sensor: ObstacleSensor = None
            self.back_obstacle_sensor: ObstacleSensor = None
        # - LEDs
        if self.use_LEDs:
            self.front_LEDs: List[ExternalLED] = [
                ExternalLED(
                    pin_number=driving_config[DrivingConfig.LEDs_FRONT.value][DrivingConfig.LEDs_FRONT_LEFT.value][DrivingConfig.LED_PIN_NUMBER.value],
                    board_mode=DrivingUtils.get_board_mode(driving_config[DrivingConfig.LEDs_FRONT.value][DrivingConfig.LEDs_FRONT_LEFT.value][DrivingConfig.LED_BOARD_MODE.value])
                ),
                ExternalLED(
                    pin_number=driving_config[DrivingConfig.LEDs_FRONT.value][DrivingConfig.LEDs_FRONT_RIGHT.value][DrivingConfig.LED_PIN_NUMBER.value],
                    board_mode=DrivingUtils.get_board_mode(driving_config[DrivingConfig.LEDs_FRONT.value][DrivingConfig.LEDs_FRONT_RIGHT.value][DrivingConfig.LED_BOARD_MODE.value])
                )
            ]
            self.front_LEDs[0].start()
            self.front_LEDs[1].start()

            self.back_LEDs: List[ExternalLED] = []
            # self.back_LEDs: List[ExternalLED] = [
            #     ExternalLED(
            #         pin_number=driving_config[DrivingConfig.LEDs_BACK.value][DrivingConfig.LEDs_BACK_LEFT.value][DrivingConfig.LED_PIN_NUMBER.value],
            #         board_mode=DrivingUtils.get_board_mode(driving_config[DrivingConfig.LEDs_BACK.value][DrivingConfig.LEDs_BACK_LEFT.value][DrivingConfig.LED_BOARD_MODE.value])
            #     ),
            #     ExternalLED(
            #         pin_number=driving_config[DrivingConfig.LEDs_BACK.value][DrivingConfig.LEDs_BACK_RIGHT.value][DrivingConfig.LED_PIN_NUMBER.value],
            #         board_mode=DrivingUtils.get_board_mode(driving_config[DrivingConfig.LEDs_BACK.value][DrivingConfig.LEDs_BACK_RIGHT.value][DrivingConfig.LED_BOARD_MODE.value])
            #    )
            # ]
            # self.back_LEDs[0].start()
            # self.back_LEDs[1].start()
        else:
            self.front_LEDs: List[ExternalLED] = []
            self.back_LEDs: List[ExternalLED] = []

    def _pre_stop_method(self, **kwargs):
        try:
            self.front_wheels_motor.stop()
            self.back_wheels_motor.stop()
            if self.use_sensors:
                if self.using_front_sensor:
                    self.front_obstacle_sensor.stop()
                if self.using_back_sensor:
                    self.back_obstacle_sensor.stop()
            if self.use_LEDs:
                self.front_LEDs[0].stop()
                self.front_LEDs[1].stop()
                # self.back_LEDs[0].stop()
                # self.back_LEDs[1].stop()
            return True
        except Exception as e:
            print(f"Exception in DrivingActivity._pre_stop_method() method: {e}")
            return False

    @staticmethod
    def get_commands(**driving_config) -> List[IDrivingCommand]:
        input_commands: List[IDrivingCommand] = list()

        if InputConfig.DRIVING_COMMANDS.value not in driving_config.keys():
            return input_commands

        received_commands: List[Dict] = driving_config[InputConfig.DRIVING_COMMANDS.value]
        for command in received_commands:

            t: datetime = datetime.strptime(
                command[InputConfig.DRIVING_EXECUTION_TIME.value],
                InputConfig.DRIVING_EXECUTION_TIME_FORMAT.value
            )
            execution_time: timedelta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

            direction_type: str = command[InputConfig.DRIVING_DIRECTION_TYPE.value]

            if direction_type == DirectionType.FORWARD.value:
                wheel_angle: float = DrivingActivity.driving_turn_angle(command[InputConfig.DRIVING_WHEEL_TURN.value])
                input_commands.append(
                    ForwardDrivingCommand(
                        wheel_angle=wheel_angle,
                        execution_time=execution_time
                    )
                )
            elif direction_type == DirectionType.BACKWARD.value:
                wheel_angle: float = DrivingActivity.driving_turn_angle(command[InputConfig.DRIVING_WHEEL_TURN.value])
                input_commands.append(
                    BackwardDrivingCommand(
                        wheel_angle=wheel_angle,
                        execution_time=execution_time
                    )
                )
            elif direction_type == DirectionType.NONE.value:
                input_commands.append(
                    NoneDrivingCommand(
                        execution_time=execution_time
                    )
                )
            else:
                continue
        return input_commands

    def execution_time(self):
        return datetime.now() - self.__execution_start

    # private
    @staticmethod
    def driving_turn_angle(driving_turn: str) -> float:
        if driving_turn == DrivingTurn.NONE.value:
            return MotorConfig.SERVO_STARTING_POINT.value
        elif driving_turn == DrivingTurn.LEFT.value:
            return MotorConfig.SERVO_LEFT_TURN_POINT.value
        elif driving_turn == DrivingTurn.RIGHT.value:
            return MotorConfig.SERVO_RIGHT_TURN_POINT.value
        else:
            return MotorConfig.SERVO_STARTING_POINT.value
