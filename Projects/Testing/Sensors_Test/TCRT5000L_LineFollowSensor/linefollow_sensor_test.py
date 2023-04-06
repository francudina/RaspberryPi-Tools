import RPi.GPIO as GPIO
from time import sleep

input_pin = 4

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin, GPIO.IN)

def loop():
    print("Krecem s iteriranjem:")
    i = 0
    j = 0
    while True:
        input_data = GPIO.input(input_pin)
        if input_data == GPIO.HIGH:
            print(f" + VIDIM BOJU RAZLICITU OD CRNE: {j}")
            j += 1
        else:
            print(f" - crna boja se pojavila ili sam predalekod: {i}")
        
        i += 1
        sleep(0.3)
            

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except Exception:
        destroy()
