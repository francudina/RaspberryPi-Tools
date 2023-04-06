import RPi.GPIO as GPIO
from time import sleep

output_pin = 4

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(output_pin, GPIO.OUT)

def loop():
    while True:
        GPIO.output(output_pin, GPIO.HIGH)
        print("> Upaljen")
        sleep(1)
        GPIO.output(output_pin, GPIO.LOW)
        print("< Ugasen\n")
        sleep(2)
            

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
