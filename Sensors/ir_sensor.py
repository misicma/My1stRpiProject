import RPi.GPIO as GPIO
from time import sleep

IN_PIN    = 23
obstacle_detected = False

def setup():
    # GPIO.setmode(GPIO.BCM) #pinovi odgovaraju onom u datasheet-u
    # IN_PIN    = 23

    GPIO.setup(IN_PIN, GPIO.IN)


def detecting():
    setup()
    global obstacle_detected
    print("Starting detecting...")
    while True:
        if GPIO.input(IN_PIN):
            obstacle_detected = True
            # print("Object detected.")
        else:
            obstacle_detected = False
            # print("Nothing detected.")
        sleep(0.1) # Check the sensor 10 times per second

# detecting()