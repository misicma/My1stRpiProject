import time
import ir_sensor
import servo
import RPi.GPIO as GPIO
import datetime
import threading


class Robot:
    #Konstruktor
    def __init__(self, running=False, detection_count=0, log_file='robot_log.txt'):
        self.running = running
        self.detection_count = detection_count
        self.log_file = log_file

        self.log_history = []

        # GPIO.setmode(GPIO.BCM) #pinovi odgovaraju onom u datasheet-u
        ir_sensor.setup()
        servo.setup()

    def start(self):
        # servo.step_once(direction=1)
        self.running = True
        print("Robot je pokrenut!")

        thread = threading.Thread(target=ir_sensor.detecting, daemon=True)
        thread.start()

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                while self.running:
                    if obstacle_detected:
                        self.detection_count += 1
                        f.writelines(f"\nObject detected - running at {datetime.now().isoformat()}")
                        # print("Object detected - running")
                        # servo.rotate(1, direction=1)
                        servo.step_once(direction = 1)
                    else:
                        f.writelines(f"\nNothing detected at {datetime.now().isoformat()}")
                        print("Nothing detected.")
                    time.sleep(0.01)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            self.stop()
        # pass

    def stop(self,running=False):
        self.running = False
        print("Robot je zaustavljen!")
        # pass

    def run(self):
        self.start()
        pass

    def get_status(self):
        return{
            'running' : self.running,
            'detection_count' : self.detection_count,
            'log_file' : self.log_file
        }

