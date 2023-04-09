import sys

from Projects.AutonomousDriving.Services.Driving.DrivingUtils import DrivingUtils
from Projects.Executables.External.Motors.MotorConfig import MotorConfig
from Projects.Executables.External.Motors.ServoSG90 import ServoSG90

"""
    Servo Calibration: used to reset servo angle to starting position.
"""
if __name__ == '__main__':

    # expecting: <servo_pin_number> <board_mode>
    args = sys.argv[1:]

    print(f"# Starting servo on pin: {args[0]} with board mode: {args[1]}")
    servo: ServoSG90 = ServoSG90(
        pin_number=int(args[0]),
        board_mode=DrivingUtils.get_board_mode(args[1])
    )
    servo.start()
    print("> servo started")

    # set servo angle
    print("# starting with calibration...")
    servo.new_result(input_angle=MotorConfig.SERVO_STARTING_POINT.value)
    print("> done")

    print("# servo cleanup...")
    servo.stop()
    print("> done")
