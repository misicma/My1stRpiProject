import RPi.GPIO as GPIO
from time import sleep

IN_PIN    = 18

def setup():
    GPIO.setmode(GPIO.BCM) #pinovi odgovaraju onom u datasheet-u
    GPIO.setup(IN_PIN, GPIO.IN)

def detecting():
    setup()
    print("Starting detecting...")
    try:
        while True:
            if GPIO.input(IN_PIN):
                print("Object detected")
            sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()

detecting()