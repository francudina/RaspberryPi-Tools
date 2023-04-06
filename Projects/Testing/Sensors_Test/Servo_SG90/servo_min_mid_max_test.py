from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.tools import sin_values
from gpiozero import Servo
from time import sleep
from signal import pause

output_pin = 4

# setup
servo = Servo(output_pin)


def loop_1():    
    while True:        
        servo.min()
        print("A servo: min")
        sleep(2)
        servo.mid()
        print("B servo: mid")
        sleep(2)
        servo.max()
        print("C servo: max")
        sleep(2)
        

def loop_2():    
    while True:        
        servo.value = -1
        print("A servo: -1")
        sleep(2)
        servo.value = +1
        print("B servo: +1")
        sleep(2)
        

if __name__ == '__main__':
    loop_2()
