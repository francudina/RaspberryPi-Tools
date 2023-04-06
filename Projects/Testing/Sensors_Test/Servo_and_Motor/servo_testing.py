import RPi.GPIO as GPIO
import time
from datetime import datetime

ERROR_OFFSET = 0.5
SERVO_MIN_DUTY = 2.5 + ERROR_OFFSET  # duty cycle for 0 degrees
SERVO_MAX_DUTY = 12.5 + ERROR_OFFSET  # duty cycle for 180 degrees
MIN_ANGLE = 0  # degrees
MAX_ANGLE = 180  # degrees

servoPin = 4

 
def setup():
    # initialize GPIO Pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)

    # initialize PWM in defined GPIO Pin
    global pwmChannel
    pwmChannel = GPIO.PWM(servoPin, 50)
    pwmChannel.start(0)


# get the corresponding value from range 0 ~ 180 degrees to min ~ max duty cycle
def mapValue(value, fromLow, fromHigh, toLow, toHigh):
    return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow


# rotate the servo to a specific angle
def servoWrite(angle):
    # make sure it doesn't go beyond the angle the servo motor can rotate
    if (angle < MIN_ANGLE):
        angle = MIN_ANGLE
    elif (angle > MAX_ANGLE):
        angle = MAX_ANGLE
    pwmChannel.ChangeDutyCycle(mapValue(angle, 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY))


def one_cycle():
    # rotate from 0 ~ 180 degrees
    print(f"(i) testiranje: {datetime.now()}")
    print("# Smjer 0->90")
    for dc in range(0, 180, 1):
        print(f"  > kut: {dc}")
        servoWrite(dc)
        time.sleep(0.001)
    time.sleep(0.5)
    # rotate from 180 ~ 0 degrees
    print("# Smjer 90->0")
    for dc in range(181, -1, -1):
        print(f"  > kut: {dc}")
        servoWrite(dc)
        time.sleep(0.001)
    time.sleep(0.05)


def destroy():
    # p.stop()
    time.sleep(2.5)
    GPIO.cleanup()


def positions_testing():
    print("Testiram ...")
    # sredina
    servoWrite(60)
    
    # skretanje lijevo
    time.sleep(1.5)
    servoWrite(130)
    
    # skretanje desno
    time.sleep(1.5)
    servoWrite(0)
    
    # skretanje lijevo
    time.sleep(1.5)
    servoWrite(130)

    # sredina
    time.sleep(1.5)
    servoWrite(60)
    print("Kraj!")
    destroy()


setup()
# positions_testing()
