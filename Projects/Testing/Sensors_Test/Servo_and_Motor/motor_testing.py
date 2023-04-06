from time import sleep      # Import sleep from time
import RPi.GPIO as GPIO     # Import Standard GPIO Module

GPIO.setmode(GPIO.BCM)      # Set GPIO mode to BCM
GPIO.setwarnings(False)

# PWM Frequency
pwmFreq = 200

PIN_IN1 = 27
PIN_IN2 = 22
PIN_PWM = 23

PIN_SBY = 24

# Setup Pins for motor controller
GPIO.setup(PIN_IN1, GPIO.OUT)    # PWMA
GPIO.setup(PIN_IN2, GPIO.OUT)    # AIN2
GPIO.setup(PIN_PWM, GPIO.OUT)    # AIN1

GPIO.setup(PIN_SBY, GPIO.OUT)    # SBY

pwma = GPIO.PWM(PIN_PWM, pwmFreq)    # pin 18 to PWM
pwma.start(0)


def forward(spd):
    runMotor(spd, "forward")


def reverse(spd):
    runMotor(spd, "reverse")


def runMotor(spd, direction):
    in1 = GPIO.HIGH
    in2 = GPIO.LOW

    if(direction == "reverse"):
        in1 = GPIO.LOW
        in2 = GPIO.HIGH
    
    GPIO.output(PIN_SBY, GPIO.HIGH)
    
    GPIO.output(PIN_IN1, in1)
    GPIO.output(PIN_IN2, in2)
    pwma.ChangeDutyCycle(spd)
        

def motorStop():
    GPIO.output(PIN_SBY, GPIO.LOW)
    # GPIO.output(PIN_IN1, GPIO.LOW)
    # GPIO.output(PIN_IN2, GPIO.LOW)


def main(args=None):
    while True:
        print("forward")
        forward(50)     # run motor forward
        sleep(2)        # ... for 2 seconds
        motorStop()     # ... stop motor
        sleep(.25)      # delay between motor runs

        print("reverse")
        reverse(50)     # run motor in reverse
        sleep(2)        # ... for 2 seoconds
        motorStop()     # ... stop motor
        sleep(.25)      # delay between motor runs


if __name__ == "__main__":
    main()
