import sys
from time import sleep
from datetime import datetime

import RPi.GPIO as GPIO


def event_detected(channel):
    state = GPIO.input(channel)
    print(f"something detected: {state}")
    if state == GPIO.LOW:
        print(f"\t+ event detected on channel '{channel}' at {datetime.utcnow().strftime('%H:%M:%S.%f')}")


def setup(obstacle_sensor_pin: int):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(obstacle_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(obstacle_sensor_pin, GPIO.FALLING, callback=event_detected, bouncetime=250)


def loop():
    while True:
        sleep(0.01)
            

if __name__ == '__main__':

    args = sys.argv[1:]
    obstacle_sensor_pin = int(args[0])

    setup(obstacle_sensor_pin)
    try:
        loop()
    except Exception:
        GPIO.remove_event_detect(obstacle_sensor_pin)
        GPIO.cleanup()

