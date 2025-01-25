#!/usr/bin/env python3

# Import libraries
import RPi.GPIO as GPIO
import time
import sys
import argparse

parser=argparse.ArgumentParser()

parser.add_argument("-p", "--servo-pin", help="Board Pin number for SERVO motor", required= False, default= "8")
parser.add_argument("-a", "--angle", help="Angle to move to", required= False, default= "0")
parser.add_argument("-f", "--from_angle", help="Angle to move from", required= False)

args=parser.parse_args()
servo_pin: int = int(args.servo_pin)
to_angle: int = int(args.angle)
from_angle: int = int(args.from_angle) if args.from_angle else to_angle

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

def setup_servo(pin: int) -> GPIO.PWM:
    """
    Set up a GPIO pin for PWM control of a servo.

    Args:
        pin (int): The GPIO pin number to use.

    Returns:
        GPIO.PWM: The PWM object for the servo.
    """
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)  # 50Hz pulse
    return servo

servo = setup_servo(servo_pin)

# Start PWM running, with value of 0 (pulse off)
servo.start(0)

def set_angle(angle: int):
    if angle == 0:
        angle = -1
    servo.ChangeDutyCycle(2+(angle/18))

try:
    if from_angle != to_angle:
        step = 3 if to_angle > from_angle else -3
        for angle in range(from_angle, to_angle, step):
            set_angle(angle)
            time.sleep(0.1)
    else:
        set_angle(to_angle)
finally:
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)