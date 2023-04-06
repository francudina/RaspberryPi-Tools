import RPi.GPIO as GPIO
from time import sleep

ObstaclePin = 4

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ObstaclePin, GPIO.IN)

def loop():
    print("Krecem s iteriranjem:")
    i = 0
    j = 0
    while True:
        input_data = GPIO.input(ObstaclePin)
        # print(f"< dobio sam: {input_data}")
        # detected = GPIO.event_detected(ObstaclePin)
        if input_data == GPIO.LOW:
            print(f" + VIDIM NESTO: {j}")
            j += 1
        else:
            print(f" - nisam nista primjetio: {i}")
        
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
