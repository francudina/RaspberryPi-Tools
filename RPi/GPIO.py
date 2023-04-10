"""

RPi.GPIO library only for testing purposes
    stackoverflow: https://raspberrypi.stackexchange.com/questions/34119/gpio-library-on-windows-while-developing

"""

import time
import random
import threading
from threading import Event

BOARD = 1
BCM = 2

OUT = 1
IN = 1

HIGH = 1
LOW = 0

RISING = 1
FALLING = 0

PUD_UP = 1
PUD_DOWN = 0

event_threads: {} = {}


class PwdTmp:

    def __init__(self, **kwargs):
        pass

    def start(self, a=None, **kwargs):
        pass

    def ChangeDutyCycle(self, angle: int):
        pass


def setmode(mode=None):
    print("setmode:", mode)


def setup(a: int, b=None, pull_up_down=None):
    print("setup:", a, b, pull_up_down)


def input(a: int, b=None):
    # print("input:", a, b)
    return LOW


def output(a: int, b=None):
    pass
    # print("output:", a, b)


def cleanup(a: int):
    print("cleanup:", a)


def setwarnings(flag: bool=None):
    print("setwarnings:", flag)


"""
Mocking sensor readings with uniform random number generator. 
If value is less then threshold then callback method is triggered.
"""
def dummy_obstacle_sensor_detector(channel: int, callback, stop_event: Event):
    threshold: float = 0.15
    sleep_between: float = 1.5
    print(f"# mocked obstacle sensor ({channel}): start")
    while not stop_event.is_set():
        if random.uniform(0, 1) < threshold:
            callback(channel)
        time.sleep(sleep_between)
    print(f"# mocked obstacle sensor ({channel}): end")


def add_event_detect(pin=None, b=None, callback=None, bouncetime=None):
    stop_event: Event = Event()
    t = threading.Thread(target=dummy_obstacle_sensor_detector, args=(pin, callback, stop_event))
    event_threads[pin] = {
        'thread': t,
        'stop_event': stop_event
    }
    t.start()


def remove_event_detect(pin=None):
    print("remove_event_detect setup: ", pin)
    event_threads[pin]['stop_event'].set()
    event_threads[pin]['thread'].join()


def PWM(a: int, b: int):
    return PwdTmp()
