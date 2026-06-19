#!/usr/bin/env python3
import ir_sensor
import servo
from robot import Robot

import RPi.GPIO as GPIO
import time
from datetime import datetime

import sys

def main():
    # Write the core logic of your program here
    GPIO.setmode(GPIO.BCM) #pinovi odgovaraju onom u datasheet-u

    # ir_sensor.setup()
    # servo.setup()

    print("Main je otpoceo radnju")

    robot = Robot()

    try:
        #Pokreni robota
        robot.start()
    except KeyboardInterrupt:
        print("Program interrupted")
        robot.stop()
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()