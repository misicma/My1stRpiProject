#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# === USER CONFIGURATION ===

DIR_PIN      = 20 #GPIO connected to DRV8825 DIR
STEP_PIN     = 21 #GPIO connected to DRV8825 STEP
M0_PIN       = 14 #GPIO connected to DRV8825 M0
M1_PIN       = 15 #GPIO connected to DRV8825 M1
M2_PIN       = 18 #GPIO connected to DRV8825 M2

STEPS_PER_REV = 200 #NEMA17 full steps per rev 
STEPS_DELAY   = 0.001 #pause between STEP pulse
# STEPS_DELAY   = 0.005 -> slow
# STEPS_DELAY   = 0.001 -> medium
# STEPS_DELAY   = 0.0005 -> fast

#Microsteps modes: (M0, M1, M2, microsteps per full step)
MICROSTEP_MODES = {
    'full':         (0, 0, 0,  1),
    'half':         (1, 0, 0,  2),
    'quarter':      (0, 1, 0,  4),
    'eighth':       (1, 1, 0,  8),
    'sixteenth':    (0, 0, 1, 16),
    'thirty_second':(1, 0, 1, 32),
}

#Choose you mode here:
MODE = 'full'

def setup():
    GPIO.setmode(GPIO.BCM) #Postavlja brojeve po pinovima
    for pin in (DIR_PIN, STEP_PIN, M0_PIN, M1_PIN, M2_PIN):
        GPIO.setup(pin, GPIO.OUT)

    # Apply microstep mode
    m0, m1, m2, _ = MICROSTEP_MODES[MODE] #Postavili smo vrijednosti na ove varijable sa lijeve strane
    GPIO.output(M0_PIN, GPIO.HIGH if m0 else GPIO.LOW)
    GPIO.output(M1_PIN, GPIO.HIGH if m1 else GPIO.LOW)
    GPIO.output(M2_PIN, GPIO.HIGH if m2 else GPIO.LOW)

def rotate(revolutions, direction, accel_steps=50, min_delay=0.0005, max_delay=0.01):
    """Rotate with acceleration from max_delay to min_delay."""
    _, _, _, microsteps = MICROSTEP_MODES[MODE]
    total_steps = int(STEPS_PER_REV * microsteps * revolutions)

    GPIO.output(DIR_PIN, GPIO.HIGH if direction else GPIO.LOW)

    while accel_steps * 2 > total_steps:
        accel_steps  = total_steps // 2 

    #Acceleration phase
    for i in range(accel_steps):
        delay = max_delay - (max_delay - min_delay) * (i / accel_steps)
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

    #Constant speed phase
    for _ in range(total_steps - 2 * accel_steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(min_delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(min_delay)

    #Deceleration phase
    for i in range(accel_steps, 0, -1): # mpr 5 4 3 2 1
        delay = max_delay - (max_delay - min_delay) * (i / accel_steps)
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)


def main():
    setup()
    print(f"Mode: {MODE}, {MICROSTEP_MODES} microsteps/full step") #IZMIJENI
    try:
        while True:
            print("Rotating orward 360°...")
            rotate(1, direction = 1)
            time.sleep(1)

            print("Rotating backward 360°...")
            rotate(1, direction = 0)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        GPIO.cleanup() #konstantno resetuje koriscene pinove u slucaju da ih nismo zamijenili sa nekim drugim
        print("Done. GPIO cleaned up")

if __name__ == "__main__":
    main()