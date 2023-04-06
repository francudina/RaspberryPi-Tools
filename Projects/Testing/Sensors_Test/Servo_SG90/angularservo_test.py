from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

output_pin = 4

initial_angle = 90

min_angle = 0
max_angle = 180


def loop_1():
    servo = AngularServo(
        output_pin,
        initial_angle=initial_angle,
        min_angle=min_angle,
        max_angle=max_angle
    )
    while True:
        servo.angle = 0
        print(f"1) {servo.angle}")
        sleep(2)
        servo.angle = 180
        print(f"2) {servo.angle}")
        sleep(2)
        

def loop_2():
    servo = AngularServo(
        output_pin,
        initial_angle=initial_angle,
        min_angle=min_angle,
        max_angle=max_angle
    )
    sleep(2)
    while True:
        servo.angle = 0
        print(f"1) {servo.angle}")
        sleep(2)
        servo.angle = 180
        print(f"2) {servo.angle}")
        sleep(2)


if __name__ == '__main__':
    loop_1()
    