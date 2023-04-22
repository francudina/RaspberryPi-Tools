"""

RPi.GPIO library only for testing purposes
    stackoverflow: https://raspberrypi.stackexchange.com/questions/34119/gpio-library-on-windows-while-developing

"""
import logging
import time
import random
import threading
from threading import Event

from Projects.Executables.Utils import TimeUtils

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

# for storing threads and joining
event_threads: {} = {}

# default values for "dummy_obstacle_sensor_detector" method
DEFAULT_THRESHOLD: float = 0.15
DEFAULT_SLEEP: float = 1.5
# current values for "dummy_obstacle_sensor_detector" method - used for overrides
CURRENT_THRESHOLD: float = DEFAULT_THRESHOLD
CURRENT_SLEEP: float = DEFAULT_SLEEP


class PwdTmp:

    def __init__(self, **kwargs):
        pass

    def start(self, a=None, **kwargs):
        pass

    def ChangeDutyCycle(self, angle: int):
        pass


def setmode(mode=None):
    # logging.info("setmode:", mode)
    pass

def setup(a: int, b=None, pull_up_down=None):
    pass

def input(a: int, b=None):
    # logging.info("input:", a, b)
    return LOW


def output(a: int, b=None):
    pass
    # logging.info("output:", a, b)


def cleanup(a: int):
    # logging.info("cleanup:", a)
    pass


def setwarnings(flag: bool=None):
    # logging.info("setwarnings:", flag)
    pass


def dummy_obstacle_sensor_detector(channel: int, callback, stop_event: Event):
    """
    Mocking sensor readings with uniform random number generator.
    If value is less than threshold then callback method is triggered.
    """
    threshold: float = CURRENT_THRESHOLD
    sleep_between: float = CURRENT_SLEEP
    logging.info(f"# mocked obstacle sensor ({channel}): start ({TimeUtils.current_time()})")
    while not stop_event.is_set():
        if random.uniform(0, 1) < threshold:
            callback(channel)
        time.sleep(sleep_between)
    logging.info(f"# mocked obstacle sensor ({channel}): end ({TimeUtils.current_time()})")


def add_event_detect(pin=None, b=None, callback=None, bouncetime=None):
    stop_event: Event = Event()
    t = threading.Thread(target=dummy_obstacle_sensor_detector, args=(pin, callback, stop_event))
    event_threads[pin] = {
        'thread': t,
        'stop_event': stop_event
    }
    t.start()


def remove_event_detect(pin=None):
    logging.info(f"# remove_event_detect ({pin}) ({TimeUtils.current_time()})")
    event_threads[pin]['stop_event'].set()
    event_threads[pin]['thread'].join()


def PWM(a: int, b: int):
    return PwdTmp()
