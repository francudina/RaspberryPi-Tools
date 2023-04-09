
"""

RPi.GPIO library only for testing purposes
    stackoverflow: https://raspberrypi.stackexchange.com/questions/34119/gpio-library-on-windows-while-developing

"""

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
    print("input:", a, b)


def output(a: int, b=None):
    pass
    # print("output:", a, b)


def cleanup(a: int):
    print("cleanup:", a)


def setwarnings(flag: bool=None):
    print("setwarnings:", flag)


def add_event_detect(a=None, b=None, callback=None, bouncetime=None):
    print("add_event_detect setup: ", a, b, callback, bouncetime)


def remove_event_detect(a=None):
    print("remove_event_detect setup: ", a)


def PWM(a: int, b: int):
    return PwdTmp()
