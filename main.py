import ir_sensor
import servo

#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

import sys

def main():
    # Write the core logic of your program here
    GPIO.setmode(GPIO.BCM) #pinovi odgovaraju onom u datasheet-u

    ir_sensor.setup()
    servo.setup()
    print("Main je otpoceo radnju")
    try:
        while True:
            if GPIO.input(ir_sensor.IN_PIN):
                print("Object detected - running")
                # servo.rotate(1, direction=1)
                servo.step_once(direction = 1)
            else:
                print("Nothing detected.")
            time.sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()
    # ir_sensor.detecting()
    # servo.rotate()

main()